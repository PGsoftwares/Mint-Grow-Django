from django.shortcuts import render, redirect
from django.db.models import Min, Max, Prefetch

from categories.models import ProductCategory
from products.models import Product, ProductPriceVariation

from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


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

    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        enquiry_type = request.POST.get("enquiry_type", "").strip()
        message = request.POST.get("message", "").strip()

        if not all([
            name,
            email,
            phone,
            enquiry_type,
            message,
        ]):

            messages.error(
                request,
                "Please fill in all required fields.",
            )

            return render(
                request,
                "home/contact.html",
            )

        enquiry_type_display = dict(
            [
                ("product", "Product Enquiry"),
                ("bulk", "Bulk Order"),
                ("export", "Export Enquiry"),
                ("farmer", "Farmer Partnership"),
                ("other", "Other"),
            ]
        ).get(
            enquiry_type,
            enquiry_type,
        )

        subject = f"New Contact Enquiry - {enquiry_type_display}"

        email_message = f"""
            You have received a new enquiry from the Mint Grow website.

            Name:
            {name}

            Email:
            {email}

            Phone:
            {phone}

            Enquiry Type:
            {enquiry_type_display}

            Message:
            {message}
            """

        send_mail(
            subject,
            email_message,
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )

        messages.success(
            request,
            "Thank you! Your enquiry has been submitted successfully.",
        )

        return redirect("contact")

    return render(
        request,
        "home/contact.html",
    )