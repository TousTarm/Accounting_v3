from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

client = MongoClient("mongodb://localhost:27017/")
db = client["accounting"]        

def sum(data):
    sum = 0
    with open('keywords.json', 'r', encoding='utf-8') as f: #NACTENI KEYWORDS
        keywords = json.load(f)
        sums_by_type = {v[0]: 0 for k, v in keywords.items()}
    for row in data:
        sum += int(float(row['amount']))
        amount = int(float(row['amount']))
        type_ = row['type']
        for key, values in keywords.items():
            if type_ == values[0]:
                sums_by_type[values[0]] += amount
    
    ordered_sums = [sums_by_type[values[0]] for key, values in keywords.items()]
    ordered_sums.insert(0,sum)
    return ordered_sums
        
@app.route('/')
def home():
    return render_template('index.j2')

@app.route('/edit')
def edit():
    with open('keywords.json', 'r', encoding='utf-8') as f: #NACTENI KEYWORDS
        keywords = json.load(f)
        keywords = [[values[0], values[1]] for values in keywords.values()]
    if request.args.get('parameter') is None:
        data = list(db['srpen'].find())
        totals = sum(data)
        return render_template('edit.j2',data=data,totals=totals,keywords=keywords)
    else:
        if request.args.get('positive') and request.args.get('negative'):
            data = list(db['srpen'].find())
            totals = sum(data)
        elif request.args.get('negative'):
            data = list(db['srpen'].find({"value": "negative"}))
            totals = sum(data)
        elif request.args.get('positive'):
            data = list(db['srpen'].find({"value": "positive"}))
            totals = sum(data)
        else:
            data = list(db['srpen'].find())
            totals = sum(data)
        return render_template('edit.j2',data=data,totals=totals,keywords=keywords)
    
@app.route('/get_data/<string:object_id>', methods=['GET'])
def get_data(object_id):
    try:
        document = db['srpen'].find_one({"_id": ObjectId(object_id)})
        if document is None:
            return jsonify({"error": "Document not found"}), 404
        document['_id'] = str(document['_id'])
        return jsonify(document)
    
    except Exception as e:
        print(f"An error occurred: {e}, něco se posralo kurwa drat")
        return jsonify({"error": "An unexpected error occurred"}), 500

@app.route('/update_data', methods=['POST'])
def update_data():
    # Get the form data
    object_id = request.form.get('id')
    date = request.form.get('date')
    amount = request.form.get('amount')
    account = request.form.get('account')
    note = request.form.get('note')
    type_ = request.form.get('type')
    flag = request.form.get('flag')

    print(date,amount,account,note,type_,flag)

    db['srpen'].update_one(
        {'_id': ObjectId(object_id)},
        {
            '$set': {
                'date': date,
                'amount': amount,
                'account': account,
                'note': note,
                'type': type_,
                'flag': flag
            }
        }
    )
    return redirect(url_for('edit'))

if __name__ == "__main__":
    app.run(debug=True)