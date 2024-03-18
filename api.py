from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)



# Sample data (in-memory storage)
data = [
    {"id": 1, "name": "Alice", "age": 30},
    {"id": 2, "name": "Bob", "age": 25},
    {"id": 3, "name": "Charlie", "age": 35}
]

# Custom request parser
parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help='Name is required')
parser.add_argument('age', type=int, required=True, help='Age is required')

# Resource for CRUD operations
class SampleResource(Resource):
    def get(self, id):
        item = next((item for item in data if item['id'] == id), None)
        if item:
            return item, 200
        else:
            return {'message': 'Item not found'}, 404

    def put(self, id):
        args = parser.parse_args()
        item = next((item for item in data if item['id'] == id), None)
        if item:
            item.update(args)
            return item, 200
        else:
            return {'message': 'Item not found'}, 404

    def delete(self, id):
        global data
        item = next((item for item in data if item['id'] == id), None)
        if item:
            data = [item for item in data if item['id'] != id]
            return {'message': 'Item deleted'}, 200
        else:
            return {'message': 'Item not found'}, 404

class SampleListResource(Resource):
    def get(self):
        return data, 200

    def post(self):
        args = parser.parse_args()
        new_id = max(item['id'] for item in data) + 1
        new_item = {'id': new_id, 'name': args['name'], 'age': args['age']}
        data.append(new_item)
        return new_item, 201

api.add_resource(SampleResource, '/sample/<int:id>')
api.add_resource(SampleListResource, '/sample')

if __name__ == '__main__':
    app.run(debug=True, port=20002)




