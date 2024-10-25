from pymongo import MongoClient
import os
import csv

# Connect to MongoDB
with MongoClient("mongodb://localhost:27017/") as client:
    db = client["accounting"]
    db["srpen"].delete_many({})
    filters = db["filters"].find()  # Adjust as needed if you want specific fields
    filter_keywords = {f['string']: f for f in filters}  # Create a dictionary for quick lookup

    with open('file.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        csv_data = []
        
        for row in reader:
            csv_data.append(row)

        documents = []
        for row in csv_data[3:]:
            try:
                row[2] = int(float(row[2].replace(",", ".")))
            except ValueError:
                print(f"Skipping row due to conversion error: {row}")
                continue
            row[14] = str(row[14]).strip().lower()
            if int(row[2]) > 0:
                value = "positive"
            else:
                value = "negative"
            matched = False
            for keyword in filter_keywords.keys():
                if keyword in row[14] and keyword != "":
                    type_val = filter_keywords[keyword]['type']
                    flag_val = filter_keywords[keyword]['flag']
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
            print("Inserted data:", len(documents))
        else:
            print("No data to insert.")
