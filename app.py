from flask import Flask, request
from db import items, stores
import uuid

app = Flask(__name__)

# Endpoint to return the stores list and their items
@app.get("/stores") # http://127.0.0.1:5000/store
# When the user types this address in the browser, the `get_store()` method is executed 
# and return the list of the stores.
def get_stores():
    return {"stores": list(stores.values())}

# Endpoint to create a store from the browser client.
@app.post("/store")
def create_store():
    store_data = request.get_json() # Retrieve the json sent by the browser client.
    store_id = uuid.uuid4().hex # Just an hexadecimal random id
    store ={**store_data, "id": store_id} # Based on json data create a new dictionary element with id
    stores[store_id] = store # New store json values appended to the stores dictionary.
    return store, 201 # Return the new store and an http status that ok, accepted.

# Endpoint to create an item of a store from the browser client.
@app.post("/item")
def create_item(name):
    item_data = request.get_json() # Retrieve the json sent by the browser client.
    # Verify if the store_id sent exists in the dictionary. If not, returns and error message. 
    if item_data["store_id"] not in stores:
        return {"message": "Store not found"}, 404

    # If store_id exists, create the item.
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    
    return item, 201

# Endpoint to retrieve all items
@app.get("/item") 
def get_all_items():
    return {"items": list(items.values())}

# Endpoint to get and item in dictionary.
@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id] # Return the store based on id.
    except KeyError:
        return {"message": "Item not found"}, 404
