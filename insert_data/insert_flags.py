from pymongo import MongoClient
with MongoClient("mongodb://localhost:27017/") as client:
    db = client["accounting"]

    db["flags"].delete_many({})

    flags = {
        "manual",
        "Jídlo",
        "Moje",
        "Investování",
        "Svačina",
        "Brigáda",
        "Škola",
    }
    documents = [{"flag": t} for t in flags]
    result = db["flags"].insert_many(documents)
    print("Inserted flags:", len(documents))
