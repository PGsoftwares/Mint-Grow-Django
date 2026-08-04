from django.shortcuts import render

from django.db.models import Min, Max

from categories.models import ProductCategory
from products.models import Product


def home_view(request):

    categories = (
        ProductCategory.objects
        .filter(
            status="active",
            parent__isnull=True,
        )
        .order_by("name")
    )

    featured_products = (
        Product.objects
        .filter(
            status="active",
            featured=True,
            category__status="active",
        )
        .select_related("category")
        .annotate(
            min_price=Min("price_variations__price"),
            max_price=Max("price_variations__price"),
        )
        .order_by("-created_at")[:8]
    )

    context = {
        "categories": categories,
        "featured_products": featured_products,
    }

    return render(
        request,
        "home/index.html",
        context,
    )

def about_view(request):
    return render(request, 'home/about.html')

def contact_view(request):
    return render(request, 'home/contact.html')