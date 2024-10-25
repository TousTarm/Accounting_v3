from pymongo import MongoClient
with MongoClient("mongodb://localhost:27017/") as client:
    db = client["accounting"]

    db["types"].delete_many({})

    types = {
        "Lidl",
        "Albert",
        "McDonalds",
        "KFC",
        "Moje",
        "Tesco",
        "Patria",
        "Kebab",
        "Tipsport",
        "Billa",
        "Brigáda",
        "Škola",
        "BurgerKing",
        "Jídlo",
        "Bagetérie"
    }
    documents = [{"type": t} for t in types]
    result = db["types"].insert_many(documents)
    print("Inserted types:", len(documents))
