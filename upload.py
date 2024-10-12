from pymongo import MongoClient #KNIHOVNY
import os,csv,json

with MongoClient("mongodb://localhost:27017/") as client: #PRIPOJENI NA MONGODB
    db = client["accounting"]
    if "srpen" not in db.list_collection_names(): #VYTVORENI KOLEKCE (PODLE MESICE)
        db.create_collection("srpen")
    collection = db["srpen"]

    with open('keywords.json', 'r', encoding='utf-8') as f: #NACTENI KEYWORDS
        keywords = json.load(f)

        # MAZE VSECHNO V DATABAZI -------------------------------------
        result = collection.delete_many({})
        # MAZE VSECHNO V DATABAZI -------------------------------------

        with open('file.csv', mode='r', newline='', encoding='utf-8') as file: #NACTE A UPRAVI CSV
            reader = csv.reader(file, delimiter=';')
            csv_data = []
            for row in reader:
                csv_data.append(row)

            data = [] 
            documents = []
            for row in csv_data[3:]: #SMAZANI PRVNICH 3 ZAZNAMU

                row[2] = int(float(row[2].replace(",","."))) #UPRAVENI CISEL
                row[14] = str(row[14]).strip().lower() #UPRAVENI NOTES

                if int(row[2]) > 0:
                    value = "positive"
                else:
                    value = "negative" 

                matched = False
                for keyword, values in keywords.items():
                    if keyword in row[14]:
                        row.append(values[0])
                        row.append(values[1])
                        matched = True
                        break
                if not matched:
                    row.append("manual")
                    row.append("manual")
                
                document = {
                    'date':row[1],
                    'amount':row[2],
                    'account':row[7],
                    'note':row[14],
                    'type':row[21],
                    'flag':row[22],
                    'value':value
                }
                documents.append(document)
            if documents:
                result = db['srpen'].insert_many(documents)
                print(f"Inserted {len(result.inserted_ids)} documents into MongoDB")
            else:
                print("No data to insert.")
