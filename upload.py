from pymongo import MongoClient
import os,csv

with MongoClient("mongodb://localhost:27017/") as client:
    db = client["accounting"]
    if "data" not in db.list_collection_names():
        db.create_collection("data")
    with open('file.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        csv_data = []
        for row in reader:
            csv_data.append(row)
            print(row)
        data = []
        documents = []
        for row in csv_data[3:]:
            new_string = row[2].replace(",",".")
            row[2] = new_string
            document = {
                'date':row[1],
                'amount':int(float(row[2])),
                'account':row[7],
                'note':row[14]
            }
            documents.append(document)
        if documents:
            result = db['data'].insert_many(documents)
            print(f"Inserted {len(result.inserted_ids)} documents into MongoDB")
        else:
            print("No data to insert.")