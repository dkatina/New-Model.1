from app.blueprints.item_descs.schemas import ItemDescSchema
from app.extensions import ma
from app.models import SerialItem
from marshmallow import fields


class SerialItemSchema(ma.SQLAlchemyAutoSchema):
    description = fields.Nested(ItemDescSchema)
    class Meta:
        model = SerialItem


serial_item_schema = SerialItemSchema()
serial_items_schema = SerialItemSchema(many=True)
