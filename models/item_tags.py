from db import db

class ItemTags(db.model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    tag_id = db.column(db.Integer, db.ForeignKey("tags.id"))