from flask import Flask, jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select
from . import customers_bp
from .schemas import customer_schema, customers_schema
from app.models import Customer, db


#CREATE CUSTOMER
@customers_bp.route('/', methods=['POST'])
def create_customer():
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Customer).where(Customer.email == customer_data['email'])
    customer = db.session.execute(query).scalars().first()

    if not customer:
        new_customer = Customer(**customer_data)
        db.session.add(new_customer)
        db.session.commit()
        return customer_schema.jsonify(new_customer), 201
    return jsonify({"error": "Email already taken."}), 400


#GET ALL CUSTOMERS
@customers_bp.route('/', methods=['GET'])
def get_users():
    query = select(Customer)
    customers = db.session.execute(query).scalars().all()

    return customers_schema.jsonify(customers), 200

#UPDATE CUSTOMERS
@customers_bp.route('/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    try:
        customer_data = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    customer = db.session.get(Customer, customer_id)

    if customer:
        for field, value in customer_data.items():
            setattr(customer, field, value)
        db.session.commit()
        return customer_schema.jsonify(customer)
    return jsonify({"error": "invalid customer_id"})

#DELETE
@customers_bp.route("/<int:customer_id>", methods=['DELETE'])
def delete_customer(customer_id):
    customer = db.session.get(Customer, customer_id)

    if customer:
        db.session.delete(customer)
        db.session.commit()
        return jsonify("customer deleted"), 200
    
    return jsonify({"error": "Invalid customer_id"})