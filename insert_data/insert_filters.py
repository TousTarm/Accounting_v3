from pymongo import MongoClient
with MongoClient("mongodb://localhost:27017/") as client:
    db = client["accounting"]
    db["filters"].delete_many({})
    filters = {
    "lidl": ["Lidl", "manual"],
    "albert": ["Albert", "manual"],
    "mcdonald": ["McDonalds", "Jídlo"],
    "kfc": ["KFC", "Jídlo"],
    "tesco": ["Tesco", "manual"],
    "patria": ["Patria", "Investování"],
    "can bey": ["Kebab", "Jídlo"],
    }
    documents = [{"string": key, "type": value[0], "flag": value[1]} for key, value in filters.items()]
    db["filters"].insert_many(documents)
    print("Inserted filters:", len(documents))
