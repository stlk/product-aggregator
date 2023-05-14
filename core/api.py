from uuid import UUID

from django.shortcuts import get_object_or_404, redirect
from ninja import Router

from core.tasks import register_product_task

from .models import Offer, Product
from .schema import CreateProductSchema, OfferSchema, ProductSchema, UpdateProductSchema

router = Router()


@router.get("/", include_in_schema=False)
def some_redirect(request):
    return redirect("/api/docs")


@router.get("/products", response=list[ProductSchema])
def list_products(request):
    return Product.objects.all()


@router.post("/products", response=ProductSchema)
def create_product(request, payload: CreateProductSchema):
    product = Product.objects.create(**payload.dict())
    product_data = {
        "id": str(product.id),
        "name": product.name,
        "description": product.description,
    }
    register_product_task.delay(product_data)
    return product


@router.put("/products/{product_id}", response={200: ProductSchema, 404: None})
def update_product(request, product_id: UUID, payload: UpdateProductSchema):
    product = get_object_or_404(Product, id=product_id)
    update_data = {k: v for k, v in payload.dict().items() if v is not None}
    for key, value in update_data.items():
        setattr(product, key, value)
    product.save()
    return product


@router.delete("/products/{product_id}", response={204: None, 404: None})
def delete_employee(request, product_id: UUID):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return 204, {"success": True}


@router.get("/products/{product_id}/offers", response=list[OfferSchema])
def get_product_offers(request, product_id: UUID):
    return Offer.objects.filter(product_id=product_id).all()
