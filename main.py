from flask import Flask, jsonify, request, render_template, Blueprint

app = Flask(__name__)

items_bp = Blueprint('items', __name__, url_prefix='/items')

class ItemService:
    def __init__(self):
        self.data = [
            {'id': 1, 'name': 'Item1', 'price': 100},
            {'id': 2, 'name': 'Item2', 'price': 200}
        ]

    def get_all(self):
        return self.data

    def get_by_id(self, item_id):
        return next((item for item in self.data if item['id'] == item_id), None)

    def add(self, item_data):
        if 'name' not in item_data or 'price' not in item_data:
            return None  # Валідація
        new_item = {
            'id': max([item['id'] for item in self.data], default=0) + 1,
            'name': item_data['name'],
            'price': item_data['price']
        }
        self.data.append(new_item)
        return new_item

    def delete(self, item_id):
        self.data = [item for item in self.data if item['id'] != item_id]

    def update(self, item_id, new_data):
        item = self.get_by_id(item_id)
        if item and 'name' in new_data and 'price' in new_data:
            item.update(new_data)
            return item
        return None

item_service = ItemService()

@app.route('/')
def home():
    return render_template('index.html')

@items_bp.route('/', methods=['GET'])
def get_items():
    return jsonify(item_service.get_all())

@items_bp.route('/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = item_service.get_by_id(item_id)
    return jsonify(item) if item else (jsonify({'error': 'Item not found'}), 404)

@items_bp.route('/', methods=['POST'])
def add_item():
    new_item = item_service.add(request.json)
    return jsonify(new_item), 201 if new_item else (jsonify({'error': 'Invalid data'}), 400)

@items_bp.route('/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    if item_service.get_by_id(item_id):
        item_service.delete(item_id)
        return jsonify({'message': 'Item deleted'})
    return jsonify({'error': 'Item not found'}), 404

@items_bp.route('/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    updated_item = item_service.update(item_id, request.json)
    return jsonify(updated_item) if updated_item else (jsonify({'error': 'Invalid data or item not found'}), 400)

app.register_blueprint(items_bp)

if __name__ == '__main__':
    app.run(debug=True)
