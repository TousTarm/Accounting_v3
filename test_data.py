from pymongo import MongoClient
import os, csv

with MongoClient("mongodb://localhost:27017/") as client:
    db = client["accounting"]
    if "srpen" not in db.list_collection_names():
        db.create_collection("srpen")
    

    # MAZE VSECHNO V DATABAZI -------------------------------------
    db["srpen"].delete_many({})  # Clear all documents in "srpen"
    db["keywords"].delete_many({})  # Clear all documents in "keywords"
    # MAZE VSECHNO V DATABAZI -------------------------------------

    keywords = {
    "lidl": ["Lidl", "manual"],
    "albert": ["Albert", "manual"],
    "mcdonald": ["Mcdonalds", "Jídlo"],
    "kfc": ["KFC", "Jídlo"],
    "potraviny, davle": ["Moje", "Moje"],
    "tesco": ["Tesco", "manual"],
    "patria": ["Patria", "Investování"],
    "can bey": ["Kebab", "Jídlo"]
    }

    documents = [{"string": key, "type": value[0], "flag": value[1]} for key, value in keywords.items()]
    db["keywords"].insert_many(documents)
    print(f"Inserted {len(documents)} documents into the 'keywords' collection in the '{db.name}' database.")
    keywords_dict = {keyword["string"]: (keyword["type"], keyword["flag"]) for keyword in db["keywords"].find()}

    collection = db["srpen"]
    with open('file.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        csv_data = []
        for row in reader:
            csv_data.append(row)

        documents = []
        for row in csv_data[3:]:  # Skip first 3 rows
            row[2] = int(float(row[2].replace(",", ".")))
            row[14] = str(row[14]).strip().lower()
            if int(row[2]) > 0:
                value = "positive"
            else:
                value = "negative"

            matched = False
            for keyword, (type_val, flag_val) in keywords_dict.items():
                if keyword in row[14]:
                    row.append(type_val)
                    row.append(flag_val)
                    matched = True
                    break

            if not matched:
                row.append("manual")
                row.append("manual")

            document = {
                'date': row[1],
                'amount': row[2],
                'account': row[7],
                'note': row[14],
                'type': row[21],
                'flag': row[22],
                'value': value
            }
            documents.append(document)

        if documents:
            result = db['srpen'].insert_many(documents)
            print(f"Inserted {len(result.inserted_ids)} documents into MongoDB")
        else:
            print("No data to insert.")



