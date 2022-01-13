import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, ItemMaster, Warehouse, WarehouseItem


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
          'Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add(
          'Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    @app.route('/')
    def main_page():
        return jsonify({
            "success": True
        })

    @app.route('/items', methods=['GET'])
    def items():

        items = ItemMaster.query.all()
        formatted_items = [
          item.format() for item in items]

        if len(formatted_items) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "items": formatted_items,
            "total_items": len(formatted_items),
        })

    @app.route('/items/<int:item_id>', methods=['DELETE'])
    def delete_item(item_id):
        try:
            item = ItemMaster.query.filter(ItemMaster.id == item_id).one_or_none()

            item.delete()

            return jsonify({
                "success": True,
                "item_id": item_id
            })

        except:
            if item is None:
                abort(404)
            abort(422)

    @app.route('/items/create', methods=['POST'])
    def create_item():
        try:
            item = ItemMaster(
                description = request.json.get("description"),
                manufacturer = request.json.get("manufacturer"), 
                category = request.json.get("category"),
                weight = request.json.get("weight"),
                height = request.json.get("height"),
                length = request.json.get("length"), 
                width = request.json.get("width"),
                image_ref = request.json.get("image_ref")
            )

            item.insert()

            return jsonify({
                "success": True,
                "item_id": item.id
            })

        except:
            abort(422)

    @app.route('/items/<int:item_id>/edit', methods=['PATCH'])
    def edit_item(item_id):
        try:
            item = ItemMaster.query.filter(ItemMaster.id == item_id).one_or_none()

            item.description = request.json.get("description")
            item.manufacturer = request.json.get("manufacturer") 
            item.category = request.json.get("category")
            item.weight = request.json.get("weight")
            item.height = request.json.get("height") 
            item.length = request.json.get("length") 
            item.width = request.json.get("width")
            item.image_ref = request.json.get("image_ref")

            item.update()

            return jsonify({
                "success": True,
                "item_id": item_id
            })

        except:
            if item is None:
                abort(404)
            abort(422)

    @app.route('/warehouses', methods=['GET'])
    def warehouses():

        warehouses = Warehouse.query.all()
        formatted_whs = [
          wh.format() for wh in warehouses]

        if len(formatted_whs) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "items": formatted_whs,
            "total_items": len(formatted_whs),
        })

    @app.route('/warehouses/create', methods=['POST'])
    def create_warehouse():

        try:
            warehouse = Warehouse(
                name = request.json.get('name'),
                country = request.json.get('country'),
                city = request.json.get('city'),
                address = request.json.get('address')
            )

            warehouse.insert()

            return jsonify({
                'success': True,
                'warehouse_id': warehouse.id
            })

        except:
            abort(422)

    @app.route('/warehouses/<int:warehouse_id>/assign_item/<int:item_id>', methods=['POST'])
    def assign_item(warehouse_id, item_id):
        try:

            warehouse = Warehouse.query.filter(Warehouse.id == warehouse_id).one_or_none()
            item = ItemMaster.query.filter(ItemMaster.id == item_id).one_or_none()

            wh_item = WarehouseItem.query.filter(
                WarehouseItem.item_id == item_id, WarehouseItem.warehouse_id == warehouse_id).one_or_none()

            if wh_item is not None:
                abort(422)
           
            warehouse_item = WarehouseItem(
                warehouse_id = warehouse_id,
                item_id = item_id,
                location = request.json.get("location"), 
                quantity = request.json.get("quantity"),
                tariff = request.json.get("tariff"),
                source = request.json.get("source"),
                destination = request.json.get("destination"),
                estimated_delivery = request.json.get("estimated_delivery")
            )

            warehouse_item.insert()

            return jsonify({
                "success": True,
                "warehouse_item_id": warehouse_item.id
            })

        except:
            if item is None:
                abort(404)
            if warehouse is None:
                abort(404)
            abort(422)


    '''
    Error handlers for all expected errors
    '''

    @app.errorhandler(404)
    def notfound(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    return app


APP = create_app()


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
