from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

client = MongoClient("mongodb://localhost:27017/")
db = client["accounting"]

def sum(data):
    sum_total = 0
    # Load keywords from MongoDB 'keywords' collection
    keywords_cursor = db["keywords"].find()
    sums_by_type = {keyword["type"]: 0 for keyword in keywords_cursor}

    for row in data:
        sum_total += int(float(row['amount']))
        amount = int(float(row['amount']))
        type_ = row['type']
        
        # Refresh the keywords cursor each time to check against new type
        keywords_cursor = db["keywords"].find()
        for keyword in keywords_cursor:
            if type_ == keyword["type"]:
                sums_by_type[keyword["type"]] += amount

    # Recalculate the sums by type and create ordered sums
    ordered_sums = list(sums_by_type.values())
    ordered_sums.insert(0, sum_total)  # Insert the total sum at the start
    return ordered_sums

@app.route('/')
def home():
    return render_template('index.j2')

@app.route('/edit')
def edit():
    keywords_cursor = db["keywords"].find()
    keywords = [[keyword["type"], keyword["flag"]] for keyword in keywords_cursor]
    if request.args.get('parameter') is None:
        data = list(db['srpen'].find())
        totals = sum(data)
        return render_template('edit.j2', data=data, totals=totals, keywords=keywords)
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
        return render_template('edit.j2', data=data, totals=totals, keywords=keywords)

@app.route('/get_data/<string:object_id>', methods=['GET'])
def get_data(object_id):
    try:
        document = db['srpen'].find_one({"_id": ObjectId(object_id)})
        if document is None:
            return jsonify({"error": "Document not found"}), 404
        document['_id'] = str(document['_id'])
        return jsonify(document)

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@app.route('/update_data', methods=['POST'])
def update_data():
    object_id = request.form.get('id')
    date = request.form.get('date')
    amount = request.form.get('amount')
    account = request.form.get('account')
    note = request.form.get('note')
    type_ = request.form.get('type')
    flag = request.form.get('flag')
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

@app.route('/get_keywords', methods=['GET'])
def get_keywords():
    try:
        keywords = list(db['keywords'].find({}, {"_id": 0}))  # Fetch all keywords without _id
        return jsonify(keywords)
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == "__main__":
    app.run(debug=True)
