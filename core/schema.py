import uuid
from typing import Annotated

from ninja import Field, Schema

from .models import Product


class ProductSchema(Schema):
    id: uuid.UUID
    name: Annotated[str, Field(..., min_length=1)]
    description: Annotated[str, Field(..., min_length=1)]

    class Config:
        model = Product
        model_fields = ["id", "name", "description"]


class OfferSchema(Schema):
    id: uuid.UUID
    price: int
    items_in_stock: int


class CreateProductSchema(Schema):
    name: str
    description: str


class UpdateProductSchema(Schema):
    name: str
    description: str
