import pandas as pd

from surprise import KNNWithMeans
from surprise import Dataset
from surprise import Reader

from functools import cmp_to_key

from flask import Flask, request, jsonify

MAX_SPENDING_PER_MONTH = 25000

def generate_alternative_suggestions(expenses):
    custom_user_table = []
    for expense in expenses:
        row = [-1, expense['id'], expense['spending_per_month'] / MAX_SPENDING_PER_MONTH]
        custom_user_table.append(row)

    sim_options = {
        "name": "cosine",
        "user_based": False,
    }
    algo = KNNWithMeans(sim_options=sim_options)

    # ID затрат:
    # 1 - сигареты
    # 2 - алкоголь
    # 3 - вредная еда
    df = pd.read_csv('users_and_expenses.csv')
    df['spending_per_month'] = df['spending_per_month'].apply(lambda x: x / MAX_SPENDING_PER_MONTH)
    df.rename(columns={'spending_per_month': 'rating'}, inplace=True)
    highest_expense_id = df['item'].max()

    # ID предложений:
    # 1 - билет в кино
    # 2 - книга, фэнтези
    # 3 - книга, детектив
    # 4 - абонемент в спортзал
    # 5 - чай
    df2 = pd.read_csv('users_and_suggestions.csv')
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
    for suggestion_id in range(1, highest_suggestion_id + 1):
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

