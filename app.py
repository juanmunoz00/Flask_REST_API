from flask import Flask, request
from flask_smorest import abort
from db import items, stores
import uuid

app = Flask(__name__)

# Endpoint to return the stores list and their items
# http://127.0.0.1:5000/store
# When the user types this address in the browser, the `get_store()` method is executed 
# and return the list of the stores.
@app.get("/stores") 
def get_stores():
    return {"stores": list(stores.values())}

# Endpoint to create a store from the browser client.
# Retrieve the json sent by the browser client.
# Just an hexadecimal random id
# New store json values appended to the stores dictionary.
# Return the new store and an http status that ok, accepted.
@app.post("/store")
def create_store():
    store_data = request.get_json() 
    
    if "name" not in store_data:
        abort(
                400,
                message="Bad request. Name not specified."
            )
    
    for store in stores.values():
        if store_data["name"] == store["name"]:
            abort(400, message="Store already exists.")
    
    store_id = uuid.uuid4().hex 
    store ={**store_data, "id": store_id} 
    stores[store_id] = store 
    
    return store, 201 

# Endpoint to return a stored based on id.
@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id]
    except KeyError:
        return {"message": "Store not found."}, 404

# Endpoint to create an item of a store from the browser client.
# Retrieve the json sent by the browser client.
# Verify if the store_id sent exists in the dictionary. If not, returns and error message. 
# If store_id exists, create the item.
@app.post("/item")
def create_item():
    item_data = request.get_json()   
    
    if(
        "price" not in item_data
        or "store_id" not in item_data
        or "name" not in item_data
    ):
        abort(
            400,
            message="Bad request. Missing price, store_id or name."
        )
    
    for item in items.values():
        if(
            item_data["name"] == item["name"]
            and item_data["store_id"] == item["store_id"]
        ):
            abort(400, message=f"Item already exists.")
    
    if item_data["store_id"] not in stores:
        return abort(404, message = "Store not found.")
    
    item_id = uuid.uuid4().hex
    item = {**item_data, "id": item_id}
    items[item_id] = item
    
    return item, 201

# Endpoint to retrieve all items
@app.get("/item") 
def get_all_items():
    return {"items": list(items.values())}





# Endpoint to get and item in dictionary.
# Return the store based on id.
@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id] 
    except KeyError:
        return abort(404, message = "Item not found.")
