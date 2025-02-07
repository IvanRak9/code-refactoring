from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

data = [
    {'id': 1, 'name': 'Item1', 'price': 100},
    {'id': 2, 'name': 'Item2', 'price': 200}
]

def find_item_by_id(item_id):
    return next((item for item in data if item['id'] == item_id), None)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(data)

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = find_item_by_id(item_id)
    if item:
        return jsonify(item)
    return jsonify({'error': 'Item not found'}), 404

@app.route('/items', methods=['POST'])
def add_item():
    new_item = request.json
    new_item['id'] = len(data) + 1  # Magic number issue
    data.append(new_item)
    return jsonify(new_item), 201

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    global data
    new_data = []  # Duplicate code issue
    for item in data:
        if item['id'] != item_id:
            new_data.append(item)
    data = new_data
    return jsonify({'message': 'Item deleted'})

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = find_item_by_id(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    item.update(request.json)
    return jsonify(item)

if __name__ == '__main__':
    app.run(debug=True)
