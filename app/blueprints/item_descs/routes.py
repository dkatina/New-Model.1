from flask import Flask, jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select
from . import item_descs_bp
from .schemas import item_desc_schema, item_descs_schema
from app.models import ItemDesc, db, SerialItem
from app.extensions import limiter, cache

#CREATE item_desc
@item_descs_bp.route('/', methods=['POST'])
@limiter.limit("5/day")
def create_item_desc():
    try:
        item_desc_data = item_desc_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(ItemDesc).where(ItemDesc.name == item_desc_data['name'])
    item_desc = db.session.execute(query).scalars().first()

    if not item_desc:
        new_item_desc = ItemDesc(**item_desc_data)
        db.session.add(new_item_desc)
        db.session.commit()
        return item_desc_schema.jsonify(new_item_desc), 201
    return jsonify({"error": f"{item_desc.name} already has a description"}), 400


#GET ALL item_descS
@item_descs_bp.route('/', methods=['GET'])
def get_item_descs():
    query = select(ItemDesc)
    item_descs = db.session.execute(query).scalars().all()

    return item_descs_schema.jsonify(item_descs), 200

#UPDATE item_descS
@item_descs_bp.route('/<int:item_desc_id>', methods=['PUT'])
@limiter.limit("1/19 days")
def update_item_desc(item_desc_id):
    try:
        item_desc_data = item_desc_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    item_desc = db.session.get(ItemDesc, item_desc_id)

    if item_desc:
        for field, value in item_desc_data.items():
            setattr(item_desc, field, value)
        db.session.commit()
        return item_desc_schema.jsonify(item_desc)
    return jsonify({"error": "invalid item_desc_id"})

#DELETE
@item_descs_bp.route("/<int:item_desc_id>", methods=['DELETE'])
@limiter.limit("5/day")
def delete_item_desc(item_desc_id):
    item_desc = db.session.get(ItemDesc, item_desc_id)

    if item_desc:
        db.session.delete(item_desc)
        db.session.commit()
        return jsonify(f"Item Description {item_desc_id} deleted"), 200
    
    return jsonify({"error": "Invalid item_desc_id"})

@item_descs_bp.route("/search", methods=['GET'])
def search_item():
    name = request.args.get('item')

    query = select(ItemDesc).where(ItemDesc.name.ilike(f'%{name}%'))
    item_desc = db.session.execute(query).scalars().first()

    stock_query = select(SerialItem).where(SerialItem.description.has(name = item_desc.name), SerialItem.ticket_id == None)
    stock = len(db.session.execute(stock_query).scalars().all())

    if item_desc:
        return jsonify({
            'item': item_desc_schema.dump(item_desc),
            'stock': stock
        })
    return jsonify({"error": "No items match this search"})

