# Full Stack Shipify_VP API Backend

Shipify_VP is inventory tracking web application for a logistics company. 

Shipify_VP has a basic CRUD Functionality. You can:
1. Create inventory items
2. Edit them
3. Delete them
4. View a list of them

Also Shipify_VP has the ability to create warehouses and assign inventory items to a specific warehouse and location.

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages within the `requirements.txt` file.

## Database Setup
With Postgres running, restore a database using the `inventory.psql` file provided. From the backend folder in terminal run:
```bash
dropdb inventory
createdb inventory
psql inventory < inventory.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app
export FLASK_ENV=development
flask run
``` 

## Endpoints
1. GET '/items'
2. POST '/items/create'
3. PATCH '/items/{item_id}/edit' 
4. DELETE '/items/{item_id}'
5. GET '/warehouses'
6. POST '/warehouses/create'
7. POST '/warehouses/{warehouse_id}/assign_item/{item_id}'

GET '/items'
- Fetches a list of items, also provides an information on total number of items 
- No arguments requested
- Returns: list of items, number of total items

POST '/items/create'
- Create a new item using submitted description, manufacturer, category, weight, height, length, width, image reference
- Request arguments: description, manufacturer, category, weight, height, length, width, image_ref 
- Returns: Success value and id of created item

PATCH '/items/{item_id}/edit'
- Edit an item based on submitted new description, manufacturer, category, weight, height, length, width, image reference
- Request arguments: item_id, description, manufacturer, category, weight, height, length, width, image_ref
- Returns: Success value and id of edited item

DELETE '/items/{item_id}'
- Delete the item of the given ID if it is exists
- Request arguments: item_id
- Returns: Success value, id of deleted item

GET '/warehouses'
- Fetches a list of warehouses, also provides an information on total number of warehouses
- No arguments requested
- Returns: list of warehouses, number of total warehouses

POST '/warehouses/create'
- Create a new warehouse using submitted name, country, city, address
- Request arguments: name, country, city, address
- Returns: Success value and id of created warehouse

POST '/warehouses/{warehouse_id}/assign_item/{item_id}'
- Assign existing inventory item to existing warehouse
- Create warehouse inventory item using submitted location, quantity, tariff, source address, destination address, estimated delivery date
- Request arguments: warehouse_id, item_id, location, quantity, tariff, source, destination, estimated_delivery
- Returns: Success value and id of created warehouse_item

## Testing
To run the tests, run
```
dropdb inventory_test
createdb inventory_test
psql inventory_test < inventory.psql
python3 test_app.py
```