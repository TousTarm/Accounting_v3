from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key' # ---------------------------------------------------------------------------HARD CODED

client = MongoClient("mongodb://localhost:27017/")
db = client["accounting"]
collection = "srpen" # ---------------------------------------------------------------------------HARD CODED

# ---------------------------- INDEX ROUTE --------------------------------------------------------
@app.route('/')
def home():
    collections = db.list_collection_names()
    collections.remove('types')
    collections.remove('flags')
    collections.remove('filters')
    return render_template('index.j2',collections=collections)
# ---------------------------- SET COLLECTION
@app.route('/set_collection', methods=['POST'])
def set_collection():
    global collection
    data = request.json
    if data and 'collection_name' in data:
        collection = data['collection_name']
        return redirect(url_for('edit'))
    return 'Invalid data', 400
# ---------------------------- EDIT ROUTE --------------------------------------------------------
@app.route('/edit')
def edit():
    if request.args.get('filter') is None:
        data = list(db[collection].find())
    else:
        if request.args.get('positive') == "true":
            data = list(db[collection].find({"value": "positive"}))
        elif request.args.get('negative') == "true":
            data = list(db[collection].find({"value": "negative"}))
        else:
            data = list(db[collection].find())
    if collection == "empty":
        return render_template('edit.j2')
    else:
        return render_template('edit.j2', data=data, stats=stats)
# ---------------------------- GET TYPE 
@app.route('/get_type')
def get_types():
    types = list(db['types'].find({}, {'_id': 0}))
    return jsonify(types)
# ---------------------------- GET FLAG 
@app.route('/get_flag')
def get_flags():
    flags = list(db['flags'].find({}, {'_id': 0}))
    return jsonify(flags)
# ---------------------------- UPDATE TYPE 
@app.route('/update_type', methods=['POST'])
def update_type():
    id = request.json.get('id')
    type = request.json.get('type')
    if (type) != "manual":
        result = db[collection].update_one({'_id': ObjectId(id)}, {'$set': {'type': type,'type_status':"updated"}})
    else:
        result = db[collection].update_one({'_id': ObjectId(id)}, {'$set': {'type': type,'type_status':"manual"}})
    if result.modified_count > 0:
        return jsonify({'message': 'Update successful'}), 200
    else:
        return jsonify({'message': 'No document updated'}), 1000
# ---------------------------- UPDATE FLAG 
@app.route('/update_flag', methods=['POST'])
def update_flag():
    id = request.json.get('id')
    flag = request.json.get('flag')
    if (flag) != "manual":
        result = db[collection].update_one({'_id': ObjectId(id)}, {'$set': {'flag': flag,'flag_status':"updated"}})
    else:
        result = db[collection].update_one({'_id': ObjectId(id)}, {'$set': {'flag': flag,'flag_status':"manual"}})
    if result.modified_count > 0:
        return jsonify({'message': 'Update successful'}), 200
    else:
        return jsonify({'message': 'No document updated'}), 404
# ---------------------------- UPDATE STATUS 
@app.route('/update_status', methods=['POST'])
def update_status():
    id = request.json.get('id')
    document = db[collection].find_one({'_id': ObjectId(id)})
    if not document:
        return jsonify({'error': 'Document not found'}), 404
    current_status = document.get('status', 'OFF')
    new_status = 'off' if current_status == 'on' else 'on'
    result = db[collection].update_one({'_id': ObjectId(id)}, {'$set': {'status': new_status}})
    if result.modified_count > 0:
        return jsonify({'message': 'Update successful', 'new_status': new_status}), 200
    else:
        return jsonify({'message': 'No document updated'}), 1000
# ---------------------------- STATS ROUTE --------------------------------------------------------
@app.route('/stats')
def stats():
    data = list(db[collection].find({"status": "on"}))
    
    # dictionary to hold stats
    stats = {}

    # iterate through the data to accumulate sums by flag and type
    for row in data:
        flag = row.get('flag', 'Unknown')
        type_name = row.get('type', 'Other')
        amount = row.get('amount', 0)
        
        # if the flag doesn't exist in stats, initialize it
        if flag not in stats:
            stats[flag] = {'total': 0, 'types': {}}
        
        # accumulate the total for the flag
        stats[flag]['total'] += amount

        # accumulate the total for each type within that flag
        if type_name not in stats[flag]['types']:
            stats[flag]['types'][type_name] = 0
        stats[flag]['types'][type_name] += amount

    # transform stats dictionary into a nested list for easier display in the template
    nested_stats = [
        [flag, stats[flag]['total'], [[type_name, total] for type_name, total in stats[flag]['types'].items()]]
        for flag in stats
    ]

    return render_template('stats.j2', stats=nested_stats)
# ---------------------------- SETTINGS ROUTE --------------------------------------------------------
@app.route('/settings')
def settings():
    types = list(db['types'].find({}, {'_id': 0}))
    flags = list(db['flags'].find({}, {'_id': 0}))
    filters = list(db['filters'].find({}, {'_id': 0}))
    return render_template('settings.j2', types=types, flags=flags, filters=filters)
# ---------------------------- ADD TYPE 
@app.route('/add_type', methods=['POST'])
def add_type():
    new_type = request.json.get('type')
    if new_type:
        db['types'].insert_one({'type': new_type})
        return jsonify({'message': 'Type added successfully!'}), 201
    return jsonify({'error': 'Type cannot be empty!'}), 400
# ---------------------------- ADD FLAG 
@app.route('/add_flag', methods=['POST'])
def add_flag():
    new_flag = request.json.get('flag')
    if new_flag:
        db['flags'].insert_one({'flag': new_flag})
        return jsonify({'message': 'Flag added successfully!'}), 201
    return jsonify({'error': 'Flag cannot be empty!'}), 400

if __name__ == "__main__":
    app.run(debug=True)
