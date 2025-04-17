from flask import Flask, jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select
from . import serial_items_bp
from .schemas import serial_item_schema, serial_items_schema
from app.models import ItemDesc, SerialItem, db
from app.extensions import limiter, cache

#CREATE serial_item
@serial_items_bp.route('/<int:description_id>', methods=['POST'])
def create_serial_item(description_id):
    item_desc = db.session.get(ItemDesc, description_id)

    if item_desc:
        new_serial_item = SerialItem(description_id=description_id)
        db.session.add(new_serial_item)
        db.session.commit()
        return serial_item_schema.jsonify(new_serial_item), 201
    return jsonify({"error": f"Invlaid description_id"}), 400


#GET ALL serial_itemS
@serial_items_bp.route('/', methods=['GET'])
def get_serial_items():
    query = select(SerialItem)
    serial_items = db.session.execute(query).scalars().all()

    return serial_items_schema.jsonify(serial_items), 200

#UPDATE serial_itemS
@serial_items_bp.route('/<int:serial_item_id>', methods=['PUT'])
def update_serial_item(serial_item_id):
    try:
        serial_item_data = serial_item_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    serial_item = db.session.get(SerialItem, serial_item_id)

    if serial_item:
        for field, value in serial_item_data.items():
            setattr(serial_item, field, value)
        db.session.commit()
        return serial_item_schema.jsonify(serial_item)
    return jsonify({"error": "invalid serial_item_id"})

#DELETE
@serial_items_bp.route("/<int:serial_item_id>", methods=['DELETE'])
def delete_serial_item(serial_item_id):
    serial_item = db.session.get(SerialItem, serial_item_id)
    item = serial_item.description.name

    if serial_item:
        db.session.delete(serial_item)
        db.session.commit()
        return jsonify(f"{item} id:{serial_item_id} deleted"), 200
    
    return jsonify({"error": "Invalid serial_item_id"})


