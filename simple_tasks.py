'''
Требования к email
- Состоит из двух частей
 * первая часть - имя пользователя
 * вторая часть - доменное имя с точкой (например example.domain)
- разделитель @
Будет корректно работать проверка is_valid_email?
'''
def is_valid_email(email):
    return "@" and "." in email


# --------------
'''
Что выведет это код?
'''
def serialize(columns, values):
    dict_data = [dict(zip(columns, row)) for row in values]
    print(dict_data)

serialize(['col1', 'col2'], (('v1', 'v2', ), ('t1', 't2', ), ))

# --------------
'''Что делает тестируемое приложение?'''
import requests
import psycopg2

BASE_URL = "http://localhost:8000/animals"

conn = psycopg2.connect(
    dbname="zoo", user="zoo_user", password="secret", host="localhost", port=5432
)
conn.autocommit = True
cursor = conn.cursor()

def test_create_update_animal():
    data = {"name": "Zebra", "cage": 5, "birth_date": "2020-07-15", "sex": "F"}
    r = requests.post(BASE_URL, json=data)
    assert r.status_code == 201
    animal_id = r.json()["id"]

    cursor.execute("SELECT name, cage, birth_date, sex FROM animals WHERE id = %s", (animal_id,))
    name, cage, birth_date, sex = cursor.fetchone()
    assert name == "Zebra"
    assert cage == 5
    assert birth_date.isoformat() == "2020-07-15"
    assert sex == "F"

    update_data = {"name": "Giraffe", "cage": 9}
    r = requests.put(f"{BASE_URL}/{animal_id}", json=update_data)
    assert r.status_code == 200

    cursor.execute("SELECT name, cage FROM animals WHERE id = %s", (animal_id,))
    name, cage = cursor.fetchone()
    assert name == "Giraffe"
    assert cage == 9

# --------------
'''
Применительно к приложению ищз предыдущего задания
Корректен ли этот тест? 
'''
def test_duplicate_create_same_data():
    data = {
        "name": "Elephant",
        "cage": 8,
        "birth_date": "2010-04-01",
        "sex": "F"
    }

    r1 = requests.post(BASE_URL, json=data)
    r2 = requests.post(BASE_URL, json=data)

    assert r1.status_code == 201
    assert r2.status_code != 201

    ids = [r.json()["id"] for r in (r1, r2) if r.status_code == 201]
    assert len(set(ids)) == 1
