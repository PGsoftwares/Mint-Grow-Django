from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Min, Max, Prefetch

from django.contrib import messages
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.templatetags.static import static

from categories.models import ProductCategory
from products.models import Product, ProductPriceVariation

from .forms import HeroSliderForm
from .models import HeroSlider


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


    # Active Hero Sliders
    hero_sliders = (
        HeroSlider.objects
        .filter(
            status="active"
        )
        .order_by(
            "sort_order",
            "-created_at",
        )
    )


    context = {
        "categories": categories,
        "products": products,
        "hero_sliders": hero_sliders,
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

        name = request.POST.get(
            "name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        enquiry_type = request.POST.get(
            "enquiry_type",
            ""
        ).strip()

        message = request.POST.get(
            "message",
            ""
        ).strip()


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

        admin_email = getattr(settings, "ADMIN_EMAIL", None) or settings.DEFAULT_FROM_EMAIL
        logo_url = getattr(settings, "LOGO_URL", "") or (
            request.build_absolute_uri(static("tabler/img/logo.png")) if request else ""
        )

        email_context = {
            "name": name,
            "email": email,
            "phone": phone,
            "enquiry_type": enquiry_type,
            "enquiry_type_display": enquiry_type_display,
            "message": message,
            "admin_email": admin_email,
            "logo_url": logo_url,
        }

        # Send Admin Alert Email
        try:
            admin_subject = f"New Contact Enquiry - {enquiry_type_display}"
            admin_text = render_to_string("home/emails/contact_admin.txt", email_context)
            admin_html = render_to_string("home/emails/contact_admin.html", email_context)
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

        # Send Customer Confirmation Email
        try:
            cust_subject = "Thank You for Contacting Mint Grow"
            cust_text = render_to_string("home/emails/contact_customer.txt", email_context)
            cust_html = render_to_string("home/emails/contact_customer.html", email_context)
            cust_email_msg = EmailMultiAlternatives(
                subject=cust_subject,
                body=cust_text,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email],
            )
            cust_email_msg.attach_alternative(cust_html, "text/html")
            cust_email_msg.send(fail_silently=False)
        except Exception:
            pass

        return render(
            request,
            "home/contact.html",
            {
                "contact_success": True,
            },
        )


    return render(
        request,
        "home/contact.html",
    )


# =========================================================
# Hero Slider Management
# =========================================================


def admin_hero_slider_list_view(request):

    sliders = (
        HeroSlider.objects
        .all()
    )


    context = {
        "sliders": sliders,
    }


    return render(
        request,
        "home/admin/hero_sliders/list.html",
        context,
    )


def admin_hero_slider_create_view(request):

    if request.method == "POST":

        form = HeroSliderForm(
            request.POST,
            request.FILES,
        )


        if form.is_valid():

            form.save()


            messages.success(
                request,
                "Hero slider added successfully.",
            )


            return redirect(
                "admin_hero_slider_list"
            )


    else:

        form = HeroSliderForm()


    context = {
        "form": form,
        "page_title": "Add Hero Slider",
    }


    return render(
        request,
        "home/admin/hero_sliders/form.html",
        context,
    )


def admin_hero_slider_edit_view(request, pk):

    slider = get_object_or_404(
        HeroSlider,
        pk=pk,
    )


    if request.method == "POST":

        form = HeroSliderForm(
            request.POST,
            request.FILES,
            instance=slider,
        )


        if form.is_valid():

            form.save()


            messages.success(
                request,
                "Hero slider updated successfully.",
            )


            return redirect(
                "admin_hero_slider_list"
            )


    else:

        form = HeroSliderForm(
            instance=slider,
        )


    context = {
        "form": form,
        "slider": slider,
        "page_title": "Edit Hero Slider",
    }


    return render(
        request,
        "home/admin/hero_sliders/form.html",
        context,
    )


def admin_hero_slider_delete_view(request, pk):

    slider = get_object_or_404(
        HeroSlider,
        pk=pk,
    )


    if request.method == "POST":

        slider.delete()


        messages.success(
            request,
            "Hero slider deleted successfully.",
        )


    return redirect(
        "admin_hero_slider_list"
    )