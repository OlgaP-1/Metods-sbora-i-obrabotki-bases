from pymongo import MongoClient

def serch_user(user_name):
    client = MongoClient()
    db = client['instagram_users']
    collection = db['instagram']
    for j in collection.find({'user_to_srapy': user_name, 'subscribers': 1}):
        print(j['login'])

def serch_profil(user_name):
    client = MongoClient()
    db = client['instagram_users']
    collection = db['instagram']
    for i in collection.find({'user_to_srapy': user_name, 'his_subscriptions': 1}):
        print(i)

user_name = 'gdv.14'


