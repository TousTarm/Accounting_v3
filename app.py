from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

client = MongoClient("mongodb://localhost:27017/")
db = client["accounting"]

#--- ROUTES ------------------------------------------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.j2')

@app.route('/edit')
def edit():
    if request.args.get('filter') is None:
        data = list(db['srpen'].find())
    else:
        if request.args.get('value') == "positive":
            data = list(db['srpen'].find({"value": "positive"}))
        elif request.args.get('value') == "negative":
            data = list(db['srpen'].find({"value": "negative"}))
        else:
            data = list(db['srpen'].find())

    stats = {type['type']: 0 for type in db['types'].find()}
    for item in data:
        if item.get('type') in stats and item.get('status') == "on":
            stats[item['type']] += item['amount']

    stats = [[type_name, total] for type_name, total in stats.items()]
    return render_template('edit.j2', data=data, stats=stats)

    
@app.route('/settings')
def settings():
    types = list(db['types'].find({}, {'_id': 0}))
    flags = list(db['flags'].find({}, {'_id': 0}))
    filters = list(db['filters'].find({}, {'_id': 0}))
    return render_template('settings.j2', types=types, flags=flags, filters=filters)

# --- METHODS ------------------------------------------------------------------------------------------------
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
    id = request.json.get('id')
    type = request.json.get('type')
    if (type) != "manual":
        result = db['srpen'].update_one({'_id': ObjectId(id)}, {'$set': {'type': type,'type_status':"updated"}})
    else:
        result = db['srpen'].update_one({'_id': ObjectId(id)}, {'$set': {'type': type,'type_status':"manual"}})
    if result.modified_count > 0:
        return jsonify({'message': 'Update successful'}), 200
    else:
        return jsonify({'message': 'No document updated'}), 1000

@app.route('/update_flag', methods=['POST'])
def update_flag():
    id = request.json.get('id')
    flag = request.json.get('flag')
    if (type) != "manual":
        result = db['srpen'].update_one({'_id': ObjectId(id)}, {'$set': {'flag': flag,'flag_status':"updated"}})
    else:
        result = db['srpen'].update_one({'_id': ObjectId(id)}, {'$set': {'flag': flag,'flag_status':"manual"}})

    result = db['srpen'].update_one({'_id': ObjectId(id)}, {'$set': {'flag': flag,'flag_status':"updated"}})
    if result.modified_count > 0:
        return jsonify({'message': 'Update successful'}), 200
    else:
        return jsonify({'message': 'No document updated'}), 1000

@app.route('/get_type')
def get_types():
    types = list(db['types'].find({}, {'_id': 0}))
    return jsonify(types)

@app.route('/get_flag')
def get_flags():
    flags = list(db['flags'].find({}, {'_id': 0}))
    return jsonify(flags)

@app.route('/update_status', methods=['POST'])
def update_status():
    id = request.json.get('id')
    document = db['srpen'].find_one({'_id': ObjectId(id)})
    if not document:
        return jsonify({'error': 'Document not found'}), 404
    current_status = document.get('status', 'OFF')
    new_status = 'off' if current_status == 'on' else 'on'
    result = db['srpen'].update_one({'_id': ObjectId(id)}, {'$set': {'status': new_status}})
    if result.modified_count > 0:
        return jsonify({'message': 'Update successful', 'new_status': new_status}), 200
    else:
        return jsonify({'message': 'No document updated'}), 1000

@app.route('/get_stats')
def get_stats():
    if request.args.get('filter') is None:
        data = list(db['srpen'].find({"status":"on"},{'_id': 0}))
        print("filter je gone")
    else:
        if request.args.get('value') == "positive":
            data = list(db['srpen'].find({"value": "positive"},{"status":"on"}))
            print("positive")
        elif request.args.get('value') == "negative":
            data = list(db['srpen'].find({"value": "negative"},{"status":"on"}))
            print("negative")
        else:
            data = list(db['srpen'].find())
            print("fuck")
    
    stats = {type['type']: 0 for type in db['types'].find()}
    for item in data:
        stats[item['type']] += item['amount']

    stats_list = [[type_name, total] for type_name, total in stats.items()]
    return jsonify(stats=stats_list)


if __name__ == "__main__":
    app.run(debug=True)
