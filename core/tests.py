import json

import pytest
from django.test import Client

from .factories import OfferFactory, ProductFactory


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def product(db):
    return ProductFactory()


@pytest.fixture
def offer(product, db):
    return OfferFactory(product=product)


def test_list_products(client, product, db):
    response = client.get("/api/products")
    assert response.status_code == 200
    assert len(json.loads(response.content)) == 1


def test_create_product(client, db):
    payload = {
        "name": "Test Product",
        "description": "This is a test product",
    }
    response = client.post("/api/products", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 200
    assert "id" in json.loads(response.content)
    assert json.loads(response.content)["name"] == payload["name"]


def test_update_product(client, product, db):
    new_name = "Updated Name"
    payload = {"name": new_name, "description": "New Description"}
    response = client.put(f"/api/products/{product.id}", data=json.dumps(payload), content_type="application/json")
    assert response.status_code == 200
    assert json.loads(response.content)["name"] == new_name


def test_delete_product(client, product, db):
    response = client.delete(f"/api/products/{product.id}")
    assert response.status_code == 204


def test_get_product_offers(client, offer, db):
    response = client.get(f"/api/products/{offer.product.id}/offers")
    assert response.status_code == 200
    assert len(json.loads(response.content)) == 1
