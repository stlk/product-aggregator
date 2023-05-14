from typing import Optional, Union
from uuid import UUID

import requests
from django.conf import settings
from django.core.cache import cache
from pydantic import BaseModel, Field


class ValidationError(BaseModel):
    loc: list[Union[str, int]] = Field(..., title="Location")
    msg: str = Field(..., title="Message")
    type: str = Field(..., title="Error Type")


class HTTPValidationError(BaseModel):
    detail: list[ValidationError] = Field(..., title="Detail")


class AuthResponse(BaseModel):
    access_token: str = Field(..., title="Access Token")


class OfferResponse(BaseModel):
    id: UUID = Field(..., title="Id")
    price: int = Field(..., title="Price")
    items_in_stock: int = Field(..., title="Items In Stock")


class RegisterProductRequest(BaseModel):
    id: UUID = Field(..., title="Id")
    name: str = Field(..., title="Name")
    description: str = Field(..., title="Description")


class RegisterProductResponse(BaseModel):
    id: UUID = Field(..., title="Id")


class OffersClient:
    def __init__(self):
        self.base_url = settings.API_BASE_URL
        self.refresh_token = settings.API_REFRESH_TOKEN

    def authenticate(self) -> Optional[AuthResponse]:
        response = requests.post(
            f"{self.base_url}/api/v1/auth",
            headers={"Bearer": self.refresh_token},
        )
        if response.status_code == 201:
            return AuthResponse(**response.json())

    def get_access_token(self) -> str:
        if access_token_response := self.authenticate():
            cache.set("access_token", access_token_response.access_token, 5 * 60)
            return access_token_response.access_token
        else:
            return cache.get("access_token")

    def register_product(self, product_data) -> RegisterProductResponse:
        token = self.get_access_token()
        if not token:
            raise Exception("failed to retrieve token")
        headers = {"Bearer": token}
        response = requests.post(
            f"{self.base_url}/api/v1/products/register",
            headers=headers,
            json=product_data,
        )
        response.raise_for_status()
        return RegisterProductResponse(**response.json())

    def get_offers(self, product_id: str) -> list[OfferResponse]:
        token = self.get_access_token()
        if not token:
            raise Exception("failed to retrieve token")
        headers = {"Bearer": token}
        response = requests.get(
            f"{self.base_url}/api/v1/products/{product_id}/offers",
            headers=headers,
        )
        response.raise_for_status()
        return [OfferResponse(**offer) for offer in response.json()]
