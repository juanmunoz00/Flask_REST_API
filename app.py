from flask import Flask, request

app = Flask(__name__)

# In this version, stores will be stored in a dictionary.  
stores = [
    {
        "name": "My Store",
        "items": [
            {
                "name": "Chair",
                "price": 15.99
            }
        ]
    }
]

# Endpoint to return the stores list and their items
@app.get("/store") # http://127.0.0.1:5000/store
# When the user types this address in the browser, the `get_store()` method is executed 
# and return the list of the stores.
def get_store():
    return {"stores": stores}

# Endpoint to create a store from the browser client.
@app.post("/store")
def create_store():
    request_data = request.get_json() # Retrieve the json sent by the browser client.
    new_store = {"name": request_data["name"], "items": []} # json parsed into the new_store object.
    stores.append(new_store) # New store json values appended to the stores dictionary.
    return new_store, 201 # Return the new store and an http status that ok, accepted.

# Endpoint to create an items of a store from the browser client.
@app.post("/store/<string:name>/item")
def create_item(name):
    request_data = request.get_json() # Retrieve the json sent by the browser client.
    # Loop (sweep) the dictionary for the store name to match 
    # so the item is appended.
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return new_item, 201
    
    return {"message": "Store not found"}, 404

# Endpoint to get the store by searching from the browser client.
@app.post("/store/<string:name>")
def get_store1(name):
    # Loop (sweep) the dictionary for the store name to match.
    for store in stores:
        if store["name"] == name:
            return store, 201 # Return the store.
    
    return {"message": "Store not found"}, 404

# Endpoint to get the store by searching from the browser client.
@app.post("/store/<string:name>")
def get_item_in_store(name):
    # Loop (sweep) the dictionary for the store name to match.
    for store in stores:
        if store["name"] == name:
            return {store["items"]}, 201 # Return the item.
    
    return {"message": "Store or item not found"}, 404     