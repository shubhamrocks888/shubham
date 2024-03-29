
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="field cannot be empty")
    parser.add_argument('store_id', type=int, required=True, help="every item needs a storeid")

    # @jwt_required()
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'item not found'}

    def post(self,name):
        if ItemModel.find_by_name(name):
            return {'message':"An item with name {} already exists.".format(name)},400

        data = Item.parser.parse_args()
        item = ItemModel(name,**data)

        try:
            item.save_to_db()
        except:
            return {'message':"error occured during insertion of item"},500

        return item.json(),201

    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message':'item is deleted'}

    def put(self,name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        
        if item is None:
            try:
                item = ItemModel(name,**data)
                item.save_to_db()
            except:
                return {'message': "error occured during inserting of item"}, 500
        else:
            try:
                item.price = data['price']
            except:
                return {'message': "error occured during inserting of item"}, 500
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'item':[item.json() for item in ItemModel.query.all()]}











