from app.extensions import ma
from app.models import Service_Ticket

class TicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model= Service_Ticket
        include_fk = True


service_ticket_schema = TicketSchema()
service_tickets_schema = TicketSchema(many=True)