from accounts.decorators import admin_required
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Product

from .forms import ProductEnquiryForm
from .models import ProductEnquiry
from django.contrib import messages
from django.views.decorators.http import require_POST


def product_enquiry_view(request, slug):

    product = get_object_or_404(
        Product.objects.select_related("category"),
        slug=slug,
        status="active",
        category__status="active",
    )

    form = ProductEnquiryForm(
        request.POST or None,
        product=product,
    )

    enquiry_success = False

    if request.method == "POST":

        if form.is_valid():

            enquiry = form.save(
                commit=False,
            )

            enquiry.product = product
            enquiry.save()

            enquiry_success = True

            form = ProductEnquiryForm(
                product=product,
            )

    return render(
        request,
        "enquiries/product_enquiry.html",
        {
            "product": product,
            "form": form,
            "enquiry_success": enquiry_success,
        },
    )


@admin_required
def enquiry_list_view(request):

    enquiries = (
        ProductEnquiry.objects
        .select_related(
            "product",
            "variation",
            "product__category",
        )
        .order_by("-created_at")
    )

    return render(
        request,
        "enquiries/list.html",
        {
            "enquiries": enquiries,
        },
    )
    
@admin_required
def enquiry_detail_view(request, id):

    enquiry = get_object_or_404(
        ProductEnquiry.objects
        .select_related(
            "product",
            "variation",
            "product__category",
        ),
        id=id,
    )

    return render(
        request,
        "enquiries/detail.html",
        {
            "enquiry": enquiry,
        },
    )
    
@admin_required
@require_POST
def enquiry_mark_contacted_view(request, id):

    enquiry = get_object_or_404(
        ProductEnquiry,
        id=id,
    )

    enquiry.status = "contacted"

    enquiry.save(
        update_fields=[
            "status",
        ]
    )

    messages.success(
        request,
        "Enquiry marked as contacted successfully.",
    )

    return redirect(
        "enquiry_detail",
        id=enquiry.id,
    )


@admin_required
@require_POST
def enquiry_mark_closed_view(request, id):

    enquiry = get_object_or_404(
        ProductEnquiry,
        id=id,
    )

    enquiry.status = "closed"

    enquiry.save(
        update_fields=[
            "status",
        ]
    )

    messages.success(
        request,
        "Enquiry closed successfully.",
    )

    return redirect(
        "enquiry_detail",
        id=enquiry.id,
    )