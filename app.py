from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

client = MongoClient("mongodb://localhost:27017/")
db = client["accounting"]

@app.route('/')
def home():
    return render_template('index.j2')

@app.route('/edit')
def edit():
    if request.args.get('filter') is None:
        data = list(db['srpen'].find())
        return render_template('edit.j2', data=data)
    else:
        if request.args.get('value') == "positive":
            data = list(db['srpen'].find({"value": "positive"}))
        elif request.args.get('value') == "negative":
            data = list(db['srpen'].find({"value": "negative"}))
        else:
            data = list(db['srpen'].find())
        return render_template('edit.j2', data=data)

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
    flag_ = request.form.get('flag')
    db['srpen'].update_one(
        {'_id': ObjectId(object_id)},
        {
            '$set': {
                'date': date,
                'amount': amount,
                'account': account,
                'note': note,
                'type': type_,
                'flag': flag_
            }
        }
    )
    return redirect(url_for('edit'))

@app.route('/get_type')
def get_types():
    types = list(db['types'].find({}, {'_id': 0}))
    return jsonify(types)

@app.route('/get_flag')
def get_flags():
    flags = list(db['flags'].find({}, {'_id': 0}))
    return jsonify(flags)

if __name__ == "__main__":
    app.run(debug=True)
