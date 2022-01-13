import os
from sqlalchemy import Column, String, Integer, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ.get('DATABASE_URL')
if not database_path:
    database_name = "inventory"
    database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Inventory Item

'''


class ItemMaster(db.Model):

    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    description = Column(String(80), unique=True)
    manufacturer = Column(String(80), nullable=False)
    category = Column(String(80), nullable=False)
    weight = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    length = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    image_ref = Column(String(500))
    whitems = relationship('WarehouseItem', cascade="all,delete",backref='whitemitem',lazy=True)


    def __init__(self, description, manufacturer, category, weight,
                    height, length, width, image_ref):
   
        self.description = description
        self.manufacturer = manufacturer
        self.category = category
        self.weight = weight
        self.height = height
        self.length = length
        self.width = width
        self.image_ref = image_ref

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'description': self.description,
            'manufacturer': self.manufacturer, 
            'category': self.category,
            'weight': self.weight,
            'height': self.height, 
            'length': self.length, 
            'width': self.width,
            'image_ref': self.image_ref
        }


'''
Warehouse

'''


class Warehouse(db.Model):

    __tablename__ = 'warehouses'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True)
    country = Column(String(80), nullable=False)
    city = Column(String(80), nullable=False)
    address = Column(String(120), nullable=False)
    whitems = relationship('WarehouseItem', cascade="all,delete",backref='whitemwh',lazy=True)

    def __init__(self, name, country, city, address):
        self.name = name
        self.country = country
        self.city = city
        self.address = address

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'country': self.country,
            'city': self.city,
            'address': self.address
        }


'''
Item in warehouse

'''


class WarehouseItem(db.Model):

    __tablename__ = 'warehouse_items'

    id = Column(Integer, primary_key=True)
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    location = Column(String(120), nullable=False)
    quantity = Column(Integer, nullable=False)
    tariff = Column(Float, nullable=False)
    source = Column(String(240), nullable=False)
    destination = Column(String(240), nullable=False)
    estimated_delivery = Column(Date(), nullable=False)

    
    def __init__(self, warehouse_id, item_id, location, quantity, tariff, 
                    source, destination, estimated_delivery):
        self.warehouse_id = warehouse_id
        self.item_id = item_id
        self.location = location
        self.quantity = quantity
        self.tariff = tariff
        self.source = source
        self.destination = destination
        self.estimated_delivery = estimated_delivery

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'warehouse_id': self.warehouse_id,
            'item_id': self.item_id,
            'location': self.location, 
            'quantity': self.quantity,
            'tariff': self.tariff,
            'source': self.source,
            'destination': self.destination,
            'estimated_delivery': self.estimated_delivery
        }
