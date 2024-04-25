import json
import requests
import pytest

@pytest.fixture
def api_url():
    return "http://localhost:7005/analyze"

def test_analysis_success(api_url):
    """ Тест успешного анализа данных """
    data = {'expenses': [{'id': 1, 'spending_per_month': 199}]}
    response = requests.post(api_url, json=data)
    assert response.status_code == 200
    assert 'suggestions' in response.json()

def test_empty_data(api_url):
    """ Тест на отправку пустых данных """
    data = {}
    response = requests.post(api_url, json=data)
    assert response.status_code == 405

def test_incomplete_data(api_url):
    """ Тест на отправку неполных данных """
    data = {'expenses': [{'id': 1}]}  # Отсутствует 'spending_per_month'
    response = requests.post(api_url, json=data)
    assert response.status_code == 405

def test_invalid_data_type(api_url):
    """ Тест на отправку данных неверного типа """
    data = {'expenses': [{'id': 'one', 'spending_per_month': 'two hundred'}]}
    response = requests.post(api_url, json=data)
    assert response.status_code == 405

def test_large_data(api_url):
    """ Тест на обработку больших данных """
    data = {'expenses': [{'id': i, 'spending_per_month': i*100} for i in range(1000)]}
    response = requests.post(api_url, json=data)
    assert response.status_code == 200

def test_stress(api_url):
    """ Стресс-тестирование с множественными запросами """
    data = {'expenses': [{'id': 1, 'spending_per_month': 199}]}
    responses = [requests.post(api_url, json=data) for _ in range(100)]
    assert all(response.status_code == 200 for response in responses)

def test_sql_injection(api_url):
    """ Тест на SQL-инъекцию """
    data = {'expenses': [{'id': 1, 'spending_per_month': 199, 'name': "'; DROP TABLE users;--"}]}
    response = requests.post(api_url, json=data)
    assert response.status_code == 405  # Предполагаем, что запрос будет отклонен


#Установите необходимые зависимости (pytest и requests), если они ещё не установлены.
#Сохраните код в файл с именем test_flask_module.py.
#Убедитесь, что ваш Flask-сервер запущен на localhost:7005.
#запустите тесты, выполнив команду pytest test_flask_module.py в терминале.