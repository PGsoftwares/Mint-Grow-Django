from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from accounts.decorators import admin_required

from .forms import ProductCategoryForm
from .models import ProductCategory

from products.models import Product

from django.db.models import Min, Max


def public_category_list_view(request):
    categories = (
        ProductCategory.objects
        .filter(
            status="active",
            parent__isnull=True,
        )
        .prefetch_related("children")
        .order_by("name")
    )

    return render(
        request,
        "categories/public_list.html",
        {
            "categories": categories,
        },
    )

def public_category_products_view(request, slug):

    category = get_object_or_404(
        ProductCategory,
        slug=slug,
        status="active",
    )

    category_ids = [category.id]

    if category.children.exists():
        category_ids.extend(
            category.children.filter(
                status="active"
            ).values_list(
                "id",
                flat=True,
            )
        )

    products = (
        Product.objects
        .select_related("category")
        .filter(
            category_id__in=category_ids,
            status="active",
        )
        .annotate(
            min_price=Min("price_variations__price"),
            max_price=Max("price_variations__price"),
        )
        .order_by("-created_at")
    )

    return render(
        request,
        "categories/public_products.html",
        {
            "category": category,
            "products": products,
        },
    )
      
@admin_required
def category_list_view(request):
    categories = (
        ProductCategory.objects
        .select_related("parent")
        .prefetch_related("children")
        .all()
    )

    return render(
        request,
        "categories/list.html",
        {
            "categories": categories,
        },
    )


@admin_required
def category_create_view(request):
    form = ProductCategoryForm(
        request.POST or None,
        request.FILES or None,
    )

    if request.method == "POST" and form.is_valid():
        category = form.save()

        messages.success(
            request,
            f'"{category.name}" created successfully.',
        )

        return redirect("category_list")

    if request.method == "POST":
        messages.error(
            request,
            "Please correct the errors below.",
        )

    return render(
        request,
        "categories/create.html",
        {
            "form": form,
        },
    )


@admin_required
def category_update_view(request, id):
    category = get_object_or_404(
        ProductCategory,
        pk=id,
    )

    old_image = (
        category.image.name
        if category.image
        else None
    )

    form = ProductCategoryForm(
        request.POST or None,
        request.FILES or None,
        instance=category,
    )

    if request.method == "POST" and form.is_valid():
        updated_category = form.save()

        new_image = request.FILES.get("image")

        if new_image and old_image:
            storage = updated_category.image.storage

            if (
                old_image != updated_category.image.name
                and storage.exists(old_image)
            ):
                storage.delete(old_image)

        messages.success(
            request,
            f'"{updated_category.name}" updated successfully.',
        )

        return redirect("category_list")

    if request.method == "POST":
        messages.error(
            request,
            "Please correct the errors below.",
        )

    return render(
        request,
        "categories/update.html",
        {
            "form": form,
            "category": category,
        },
    )


@admin_required
@require_POST
def category_toggle_status_view(request, id):
    category = get_object_or_404(
        ProductCategory,
        pk=id,
    )

    if category.status == ProductCategory.STATUS_ACTIVE:
        category.status = ProductCategory.STATUS_INACTIVE
        action = "deactivated"
    else:
        category.status = ProductCategory.STATUS_ACTIVE
        action = "activated"

    category.save(
        update_fields=[
            "status",
            "updated_at",
        ]
    )

    messages.success(
        request,
        f'"{category.name}" {action} successfully.',
    )

    return redirect("category_list")


@admin_required
def category_delete_view(request, id):
    category = get_object_or_404(
        ProductCategory,
        pk=id,
    )

    category_name = category.name

    if category.image:
        category.image.delete(save=False)

    category.delete()

    messages.success(
        request,
        f'"{category_name}" deleted successfully.',
    )

    return redirect("category_list")