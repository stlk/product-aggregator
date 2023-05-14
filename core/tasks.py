from scheduler import job

from core.offers_client import OffersClient

from .models import Offer, Product


@job
def update_offers():
    client = OffersClient()
    for product in Product.objects.all():
        offers = client.get_offers(str(product.id))
        received_offer_ids = []
        for offer in offers:
            received_offer_ids.append(offer.id)
            Offer.objects.update_or_create(
                id=offer.id,
                defaults={
                    "price": offer.price,
                    "items_in_stock": offer.items_in_stock,
                    "product": product,
                },
            )
        # Delete offers that were not in the received data
        Offer.objects.filter(product=product).exclude(id__in=received_offer_ids).delete()


@job
def register_product_task(product_data):
    client = OffersClient()
    client.register_product(product_data)
