from decimal import Decimal

from products.models import Product


class Cart:

    def __init__(self, request):

        self.session = request.session

        cart = self.session.get("cart")

        if not cart:
            cart = self.session["cart"] = {}

        self.cart = cart


    def add(
        self,
        product,
        variation,
        quantity=1,
        override_quantity=False,
    ):

        cart_key = str(variation.id)

        if cart_key not in self.cart:

            self.cart[cart_key] = {
                "product_id": product.id,
                "variation_id": variation.id,
                "quantity": 0,
                "price": str(variation.price),
            }

        if override_quantity:

            self.cart[cart_key]["quantity"] = quantity

        else:

            self.cart[cart_key]["quantity"] += quantity

        self.save()


    def remove(self, variation_id):

        cart_key = str(variation_id)

        if cart_key in self.cart:

            del self.cart[cart_key]

            self.save()


    def save(self):

        self.session.modified = True


    def clear(self):

        self.session["cart"] = {}

        self.session.modified = True


    def __len__(self):

        return sum(
            item["quantity"]
            for item in self.cart.values()
        )


    def get_total_price(self):

        return sum(
            Decimal(item["price"]) * item["quantity"]
            for item in self.cart.values()
        )