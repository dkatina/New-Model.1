from app.extensions import ma
from app.models import ItemDesc


class ItemDescSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ItemDesc

item_desc_schema = ItemDescSchema()
item_descs_schema = ItemDescSchema(many=True)
