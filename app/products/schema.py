from app.extensions import ma
from app.products.models.product_model import Product


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True


# Single product
product_schema = ProductSchema()

# Multiple products
products_schema = ProductSchema(many=True)