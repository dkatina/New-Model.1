from flask import Flask, jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select
from . import mechanics_bp
from .schemas import mechanic_schema, mechanics_schema, login_schema, mechnic_activity_schema, update_mechanic_schema
from app.models import Mechanic, db
from app.extensions import limiter, cache
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.auth import encode_token, token_required


#LOGIN
@mechanics_bp.route('/login', methods=['POST'])
@limiter.limit("5 per 10 minutes")
def login():
    try:
        creds = login_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Mechanic).where(Mechanic.email == creds['email'])
    mechanic = db.session.execute(query).scalars().first()

    if mechanic and check_password_hash(mechanic.password, creds['password']):
        token = encode_token(mechanic.id)
        return jsonify({"token": token})
    return jsonify({"error": "Invalid email or password"})



#CREATE mechanic
@mechanics_bp.route('/', methods=['POST'])
@limiter.limit("50/day")
def create_mechanic():
    try:
        mechanic_data = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    query = select(Mechanic).where(Mechanic.email == mechanic_data['email'])
    mechanic = db.session.execute(query).scalars().first()

    mechanic_data['password'] = generate_password_hash(mechanic_data['password'])

    if not mechanic:
        new_mechanic = Mechanic(**mechanic_data)
        db.session.add(new_mechanic)
        db.session.commit()
        return mechanic_schema.jsonify(new_mechanic), 201
    return jsonify({"error": "Email already taken."}), 400


#GET ALL mechanicS
@mechanics_bp.route('/', methods=['GET'])
@cache.cached(timeout=600)
def get_mechanincs():
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()

    return mechanics_schema.jsonify(mechanics), 200

#UPDATE mechanicS
@mechanics_bp.route('/', methods=['PUT'])
@token_required
def update_mechanic():
    try:
        mechanic_data = update_mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    mechanic_id = request.mechanic_id
    
    mechanic = db.session.get(Mechanic, mechanic_id)

    if mechanic:
        for field, value in mechanic_data.items():
            setattr(mechanic, field, value)
        db.session.commit()
        return mechanic_schema.jsonify(mechanic)
    return jsonify({"error": "invalid mechanic_id"})

#DELETE
@mechanics_bp.route("/", methods=['DELETE'])
@limiter.limit("50/day")
@token_required
def delete_mechanic():
    mechanic = db.session.get(Mechanic, request.mechanic_id)

    if mechanic:
        db.session.delete(mechanic)
        db.session.commit()
        return jsonify("mechanic deleted"), 200
    
    return jsonify({"error": "Invalid mechanic_id"})


@mechanics_bp.route("/activity-tracker", methods=["GET"])
def get_active_mechanics():
    query = select(Mechanic)
    mechanics = db.session.execute(query).scalars().all()

    mechanics.sort(key= lambda mechanic: len(mechanic.tickets))

    return jsonify({"mesage": "success",
                    "mechanics": mechnic_activity_schema.dump(mechanics[::-1])}), 200


#QUERY PARAMETER ENDPOINT
@mechanics_bp.route("/search", methods=['GET'])
def search_mechanic():
    name = request.args.get('search')

    query = select(Mechanic).where(Mechanic.name.ilike(f'%{name}%'))
    mechanics = db.session.execute(query).scalars().all()
    return jsonify({"mechanics": mechanics_schema.dump(mechanics)})

#Route with Path Parameter
@mechanics_bp.route('/<int:mechanic_id>', methods=['GET'])
def get_mechanic(mechanic_id):
    mechanic = db.session.get(Mechanic, mechanic_id)

    if mechanic:
        return mechanic_schema.jsonify(mechanic), 200
    return jsonify({"error": "Invalid mechanic_id"}), 400


@mechanics_bp.route('/pagenated', methods=['GET'])
def get_mechanincs_pagenation():
    page = int(request.args.get("page"))
    per_page = int(request.args.get("per_page"))

    query = select(Mechanic)
    mechanics = db.paginate(query, page=page, per_page=per_page)
    return mechanics_schema.jsonify(mechanics)

   