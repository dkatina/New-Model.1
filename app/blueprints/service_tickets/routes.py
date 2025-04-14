from flask import Flask, jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select
from . import service_tickets_bp
from .schemas import service_ticket_schema, service_tickets_schema
from app.models import Customer, Mechanic, Service_Ticket, db
from app.blueprints.mechanics.schemas import mechanics_schema
from app.extensions import limiter

#url_prefix = /service-tickets

#Create Service Ticket
@service_tickets_bp.route("/", methods=['POST'])
@limiter.limit("20/hour")
def create_ticket():
    try:
        ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    customer = db.session.get(Customer, ticket_data['customer_id'])

    if customer:
        new_ticket = Service_Ticket(**ticket_data)
        db.session.add(new_ticket)
        db.session.commit()
        return service_ticket_schema.jsonify(new_ticket), 201
    
    return jsonify({"error": "Invalid customer_id"}), 400

#Add mechanic to ticket
@service_tickets_bp.route("/<int:ticket_id>/add-mechanic/<int:mechanic_id>", methods=['PUT'])
def add_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(Service_Ticket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if ticket and mechanic:
        if mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic)
            db.session.commit()
            return jsonify({
                'message': f"Mechanic {mechanic.name} successfully added to ticket",
                'service_ticket': service_ticket_schema.dump(ticket),
                'mechanics': mechanics_schema.dump(ticket.mechanics)
            }), 200
        return jsonify({"error": "Mechanic already assigned to this ticket."}), 400
    return jsonify({"error": "Invalid ticket_id or mechanic_id."}), 400


#Remove mechanic from ticket
@service_tickets_bp.route("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>", methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = db.session.get(Service_Ticket, ticket_id)
    mechanic = db.session.get(Mechanic, mechanic_id)

    if ticket and mechanic:
        if mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)
            db.session.commit()
            return jsonify({
                'message': f"Mechanic {mechanic.name} successfully removed from ticket",
                'service_ticket': service_ticket_schema.dump(ticket),
                'mechanics': mechanics_schema.dump(ticket.mechanics)
            }), 200
        return jsonify({"error": "Mechanic not included on this ticket."}), 400
    return jsonify({"error": "Invalid ticket_id or mechanic_id."}), 400


#GET SPECIFIC TICKET
@service_tickets_bp.route("/<int:ticket_id>", methods=['GET'])
def get_ticket(ticket_id):
    ticket = db.session.get(Service_Ticket, ticket_id)
  
    if ticket:
        return jsonify({
                'service_ticket': service_ticket_schema.dump(ticket),
                'mechanics': mechanics_schema.dump(ticket.mechanics)
            }), 200
    return jsonify({"error": "Invalid ticket_id."}), 400