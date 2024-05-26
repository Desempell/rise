import pandas as pd
import pandas.io.sql as pd_sql
import psycopg2
from psycopg2._psycopg import connection

from surprise import KNNWithMeans
from surprise import Dataset
from surprise import Reader

from functools import cmp_to_key

from flask import Flask, request, jsonify

MAX_SPENDING_PER_MONTH = 25000

def generate_alternative_suggestions(expenses):
    conn = psycopg2.connect(
        dbname='postgres',
        host="localhost",
        user='postgres',
        password='admin',
        port='5432'
    )
    with conn:
        # make our own user
        custom_user_table = []
        for expense in expenses:
            row = [-1, expense['id'], expense['spending_per_month'] / MAX_SPENDING_PER_MONTH]
            custom_user_table.append(row)

        sim_options = {
            "name": "cosine",
            "user_based": False,
        }
        algo = KNNWithMeans(sim_options=sim_options)

        # read expenses from db and turn spending amounts into ratings
        df = pd_sql.read_sql_query('SELECT user_id as user, type_id as item, amount as spending_per_month FROM expenses', conn)
        df['spending_per_month'] = df['spending_per_month'].apply(lambda x: x / MAX_SPENDING_PER_MONTH)
        df.rename(columns={'spending_per_month': 'rating'}, inplace=True)
        highest_expense_id = df['item'].max()

        # read suggestions from db
        df2 = pd_sql.read_sql_query('SELECT user_id as user, suggestion_type_id as item, rating as rating FROM suggestions', conn)
        highest_suggestion_id = df2['item'].max()
        df2['item'] = df2['item'].add(highest_expense_id)
        df = pd.concat(objs=[df, df2], ignore_index=True)

        df_custom_user = pd.DataFrame(custom_user_table, columns=['user', 'item', 'rating'])
        df = pd.concat([df, df_custom_user], ignore_index=True)

        reader = Reader(rating_scale=(1, 5))
        data = Dataset.load_from_df(df[['user', 'item', 'rating']], reader)

        training_set = data.build_full_trainset()

        algo.fit(training_set)

        suggestions = list()
        for suggestion_id in range(0, highest_suggestion_id + 1):
            suggestion = algo.predict(-1, highest_expense_id + suggestion_id)
            suggestions.append({'id': suggestion_id, 'rating': suggestion.est})
        suggestions = sorted(suggestions, key=cmp_to_key(lambda x, y: y['rating'] - x['rating']))
        return suggestions

if __name__ == '__main__':
    # test_suggestions = generate_alternative_suggestions([
    #     {'id': 1, 'spending_per_month': 199}
    # ])
    # print(test_suggestions)
    
    app = Flask(__name__)

    @app.route('/analyze', methods=['POST'])
    def analyze():
        expenses = request.json['expenses']
        if expenses is not None:
            suggestions = generate_alternative_suggestions(expenses)
            return jsonify({"message": "Analysis successful", "suggestions": suggestions})
        return jsonify({"error": "Invalid input data"}), 405
    
    @app.errorhandler(Exception)
    def error_handler(error):
        return jsonify({"error": error.description}), error.code
    
    app.run(port="7005")
