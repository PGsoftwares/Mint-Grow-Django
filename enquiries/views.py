from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.templatetags.static import static

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

            variation_name = (
                enquiry.variation.name
                if enquiry.variation
                else "N/A"
            )

            admin_email = getattr(settings, "ADMIN_EMAIL", None) or settings.DEFAULT_FROM_EMAIL
            logo_url = getattr(settings, "LOGO_URL", "") or (
                request.build_absolute_uri(static("tabler/img/logo.png")) if request else ""
            )

            email_context = {
                "enquiry": enquiry,
                "product": product,
                "variation_name": variation_name,
                "admin_email": admin_email,
                "logo_url": logo_url,
            }

            # Send Admin Alert Email
            try:
                admin_subject = f"New Product Enquiry - {product.name}"
                admin_text = render_to_string("enquiries/emails/enquiry_admin.txt", email_context)
                admin_html = render_to_string("enquiries/emails/enquiry_admin.html", email_context)
                admin_email_msg = EmailMultiAlternatives(
                    subject=admin_subject,
                    body=admin_text,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[admin_email],
                )
                admin_email_msg.attach_alternative(admin_html, "text/html")
                admin_email_msg.send(fail_silently=False)
            except Exception:
                pass

            enquiry_success = True

            form = ProductEnquiryForm(
                product=product,
            )

            # Send Customer Confirmation Email
            try:
                cust_subject = f"Enquiry Received - {product.name}"
                cust_text = render_to_string("enquiries/emails/enquiry_customer.txt", email_context)
                cust_html = render_to_string("enquiries/emails/enquiry_customer.html", email_context)
                cust_email_msg = EmailMultiAlternatives(
                    subject=cust_subject,
                    body=cust_text,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[enquiry.email],
                )
                cust_email_msg.attach_alternative(cust_html, "text/html")
                cust_email_msg.send(fail_silently=False)
            except Exception:
                pass

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