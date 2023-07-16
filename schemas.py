from marshmallow import Schema, fields

# Include a nested item within a store
# but do not want to add information about the store itself
class PlainItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    store_id = fields.Str(required=True)

class PlainStoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    
class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()

# Nested fields    
class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    
class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema(), dump_only=True))    