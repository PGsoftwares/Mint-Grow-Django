from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.db.models import Q

from accounts.decorators import admin_required

from .forms import ProductForm
from .models import Product
from .models import ProductCategory

from django.core.paginator import Paginator


def public_product_list_view(request):
    selected_category = request.GET.get(
        "category",
        "",
    ).strip()

    search_query = request.GET.get(
        "search",
        "",
    ).strip()

    products_queryset = (
        Product.objects
        .select_related("category")
        .filter(
            status="active",
            category__status="active",
        )
        .order_by("-created_at")
    )

    if selected_category:
        products_queryset = products_queryset.filter(
            category__slug=selected_category,
        )

    if search_query:
        products_queryset = products_queryset.filter(
            Q(name__icontains=search_query)
            | Q(sku__icontains=search_query)
            | Q(short_description__icontains=search_query)
            | Q(description__icontains=search_query)
        )

    paginator = Paginator(
        products_queryset,
        100,
    )

    page_number = request.GET.get("page")

    products = paginator.get_page(
        page_number,
    )

    categories = (
        ProductCategory.objects
        .filter(status="active")
        .order_by("name")
    )

    context = {
        "products": products,
        "categories": categories,
        "selected_category": selected_category,
        "search_query": search_query,
    }

    return render(
        request,
        "products/public_list.html",
        context,
    )


def public_product_detail_view(request, slug):
    product = get_object_or_404(
        Product.objects.select_related("category"),
        slug=slug,
        status="active",
        category__status="active",
    )

    related_products = (
        Product.objects
        .select_related("category")
        .filter(
            category=product.category,
            status="active",
        )
        .exclude(pk=product.pk)
        .order_by("-created_at")[:3]
    )

    context = {
        "product": product,
        "related_products": related_products,
    }

    return render(
        request,
        "products/public_detail.html",
        context,
    )
    
@admin_required
def product_list_view(request):

    products = Product.objects.select_related(
        "category"
    ).order_by("-created_at")

    return render(
        request,
        "products/list.html",
        {
            "products": products,
        },
    )


@admin_required
def product_create_view(request):

    form = ProductForm(
        request.POST or None,
        request.FILES or None,
    )

    if request.method == "POST":

        if form.is_valid():
            product = form.save()

            messages.success(
                request,
                f"{product.name} created successfully!",
            )

            return redirect("product_list")

        messages.error(
            request,
            "Please correct the errors below.",
        )

    return render(
        request,
        "products/create.html",
        {
            "form": form,
        },
    )


@admin_required
def product_update_view(request, id):

    product = get_object_or_404(
        Product,
        id=id,
    )

    old_image = product.image

    form = ProductForm(
        request.POST or None,
        request.FILES or None,
        instance=product,
    )

    if request.method == "POST":

        if form.is_valid():

            product = form.save()

            if (
                old_image
                and request.FILES.get("image")
                and old_image != product.image
            ):
                old_image.delete(save=False)

            messages.success(
                request,
                f"{product.name} updated successfully!",
            )

            return redirect("product_list")

        messages.error(
            request,
            "Please correct the errors below.",
        )

    return render(
        request,
        "products/update.html",
        {
            "form": form,
            "product": product,
        },
    )


@admin_required
@require_POST
def product_toggle_status_view(request, id):

    product = get_object_or_404(
        Product,
        id=id,
    )

    if product.status == "active":

        product.status = "inactive"
        message = "Product deactivated successfully!"

    else:

        product.status = "active"
        message = "Product activated successfully!"

    product.save(
        update_fields=[
            "status",
            "updated_at",
        ]
    )

    messages.success(
        request,
        message,
    )

    return redirect("product_list")


@admin_required
def product_delete_view(request, id):

    product = get_object_or_404(
        Product,
        id=id,
    )

    if request.method == "POST":

        if product.image:
            product.image.delete(save=False)

        product.delete()

        messages.success(
            request,
            f"{product.name} deleted successfully!",
        )

        return redirect("product_list")

    return render(
        request,
        "products/delete.html",
        {
            "product": product,
        },
    )