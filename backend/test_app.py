import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, ItemMaster, Warehouse, WarehouseItem


class InventoryTestCase(unittest.TestCase):
    """This class represents the Inventory test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "inventory_test"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_item = {
            "description": "Washer",
            "manufacturer": "Samsung", 
            "category": "Appliances",
            "weight": 23.0,
            "height": 3.0,
            "length": 1.0, 
            "width": 1.0,
            "image_ref": "empty"
        }

        self.edit_item = {
            "description": "Dryer",
            "manufacturer": "Samsung", 
            "category": "Appliances",
            "weight": 23.0,
            "height": 3.0,
            "length": 1.0, 
            "width": 1.0,
            "image_ref": "empty"
        }

        self.new_warehouse = {
            "name": "825RUS",
            "country": "Russia",
            "city": "Moscow",
            "address": "25 Prospect Lenina"
        }

        self.new_warehouse_item = {
            "location": "26F", 
            "quantity": 5,
            "tariff": 300.0,
            "source": "14 Mulberry Lane Bolingbrook, IL 60440",
            "destination": "223 Crescent Lane St-Louis-de-Kent, NB E4X 4A7",
            "estimated_delivery": "4/7/2022"
        }

        self.new_bad_item = {
            "description": "TV",
            "manufacturer": "Samsung", 
            "category": "Appliances",
            "weight": 23.0,
            "height": "Three",
            "length": "One", 
            "width": 1.0,
            "image_ref": "empty"
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Tests for successful operation
    """

    def test_get_items(self):
        res = self.client().get('/items')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_items'])
        self.assertTrue(len(data['items']))

    def test_delete_item(self):
        res = self.client().delete('/items/12')
        data = json.loads(res.data)

        item = ItemMaster.query.filter(ItemMaster.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(item, None)

    def test_create_new_item(self):
        res = self.client().post("/items/create", json=self.new_item)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_edit_item(self):
        res = self.client().patch('/items/11/edit', json=self.edit_item)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_new_warehouse(self):
        res = self.client().post('/warehouses/create', json=self.new_warehouse)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_assign_item_to_warehouse(self):
        res = self.client().post(
            '/warehouses/7/assign_item/14',
            json=self.new_warehouse_item
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


    '''
    Tests for expected errors
    '''

    def test_404_if_item_does_not_exist(self):
        res = self.client().delete('/items/500')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_422_if_item_creation_fails(self):
        res = self.client().post(
            '/items/create',
            json=self.new_bad_item
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_422_if_item_editing_fails(self):
        res = self.client().patch(
            '/items/11/edit',
            json=self.new_bad_item
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_404_if_item_assigned_to_nonexisting_warehouse_(self):
        res = self.client().post(
            '/warehouses/500/assign_item/13',
            json=self.new_warehouse_item
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_422_if_item_assigned_to_the_same_warehouse_(self):
        res = self.client().post(
            '/warehouses/8/assign_item/15',
            json=self.new_warehouse_item
        )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
