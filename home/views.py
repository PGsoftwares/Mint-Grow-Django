from django.shortcuts import render
from django.db.models import Min, Max, Prefetch

from categories.models import ProductCategory
from products.models import Product, ProductPriceVariation


def home_view(request):

    categories = (
        ProductCategory.objects
        .filter(
            status="active",
            parent__isnull=True,
        )
        .order_by("name")
    )


    products = (
        Product.objects
        .filter(
            status="active",
            category__status="active",
        )
        .select_related(
            "category"
        )
        .prefetch_related(
            Prefetch(
                "price_variations",
                queryset=ProductPriceVariation.objects.order_by(
                    "price"
                ),
            )
        )
        .annotate(
            min_price=Min(
                "price_variations__price"
            ),
            max_price=Max(
                "price_variations__price"
            ),
        )
        .order_by(
            "-featured",
            "-created_at",
        )
    )


    context = {
        "categories": categories,
        "products": products,
    }


    return render(
        request,
        "home/index.html",
        context,
    )


def about_view(request):
    return render(
        request,
        "home/about.html",
    )


def contact_view(request):
    return render(
        request,
        "home/contact.html",
    )