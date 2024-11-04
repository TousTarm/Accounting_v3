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
    
@app.route('/settings')
def settings():
    types = list(db['types'].find({}, {'_id': 0}))
    flags = list(db['flags'].find({}, {'_id': 0}))
    filters = list(db['filters'].find({}, {'_id': 0}))
    return render_template('settings.j2', types=types, flags=flags, filters=filters)

@app.route('/add_type', methods=['POST'])
def add_type():
    new_type = request.json.get('type')
    if new_type:
        db['types'].insert_one({'type': new_type})
        return jsonify({'message': 'Type added successfully!'}), 201
    return jsonify({'error': 'Type cannot be empty!'}), 400

@app.route('/add_flag', methods=['POST'])
def add_flag():
    new_flag = request.json.get('flag')
    if new_flag:
        db['flags'].insert_one({'flag': new_flag})
        return jsonify({'message': 'Flag added successfully!'}), 201
    return jsonify({'error': 'Flag cannot be empty!'}), 400

@app.route('/update_type', methods=['POST'])
def update_type():
    data = request.get_json()
    if not data or 'id' not in data or 'type' not in data:
        return jsonify({'error': 'Invalid input'}), 400
    result = db['types'].update_one({'_id': data['id']},{'$set': {'type': data['type']}})
    if result.modified_count > 0:
        return jsonify({'message': 'Update successful'}), 200
    else:
        return jsonify({'message': 'No document updated'}), 404

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
