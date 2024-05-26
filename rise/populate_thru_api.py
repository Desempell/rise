import requests
import random

expense_types = [
    {'name': 'Продукты'},
    {'name': 'Транспорт'},
    {'name': 'Жильё'},
    {'name': 'Медицина'},
    {'name': 'Образование'},
    {'name': 'Развлечения'},
    {'name': 'Одежда'},
    {'name': 'Коммунальные платежи'},
    {'name': 'Техника'},
    {'name': 'Красота и здоровье'},
    {'name': 'Спорт и фитнес'}
]
for expense in expense_types:
    requests.post('http://localhost:8000/api/create-expense-type/', json={
        'name': expense['name']
    })

suggestion_types = [
    {'name': 'Продукты по акции', 'price': 250},
    {'name': 'Абонемент в фитнес-центр', 'price': 500},
    {'name': 'Курсы иностранного языка', 'price': 9000},
    {'name': 'Косметика по уходу за кожей', 'price': 2000},
    {'name': 'Лекарственные препараты', 'price': 900}
]
for suggestion in suggestion_types:
    requests.post('http://localhost:8000/api/create-suggestion-type/', json={
        'name': suggestion['name'],
        'price': suggestion['price']
    })

for i in range(4):
    session = requests.session()

    register_response = session.post('http://localhost:8000/api/register/', json={
        'username': f'user{i}',
        'password': '123456'
    }).json()
    session.post('http://localhost:8000/api/login/', json={
        'username': f'user{i}',
        'password': '123456'
    })

    for _ in range(10):
        session.post('http://localhost:8000/api/create_expenses/', json={
            'userID': register_response['user_id'],
            'date': '01/01/2023',
            'amount': random.randrange(1, 5000),
            'description': '',
            'typeID': random.randint(1, len(expense_types))
        })
    
    for suggestion_id in range(len(suggestion_types)):
        session.post('http://localhost:8000/api/create_suggestion/', json={
            'userID': register_response['user_id'],
            'description': '---',
            'saved_money': random.randrange(1, 5000),
            'rating': random.randint(1, 5),
            'typeID': random.randint(1, len(suggestion_types))
        })

    session.post('http://localhost:8000/api/logout/')
