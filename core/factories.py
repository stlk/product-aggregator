from uuid import uuid4

import factory

from .models import Offer, Product


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    id = factory.LazyFunction(uuid4)
    name = factory.Faker("word")
    description = factory.Faker("paragraph")


class OfferFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Offer

    id = factory.LazyFunction(uuid4)
    price = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    items_in_stock = factory.Faker("random_int", min=1, max=100)
    product = factory.SubFactory(ProductFactory)
