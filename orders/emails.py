import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.urls import reverse

logger = logging.getLogger(__name__)


def get_logo_url(request=None):
    """
    Returns the URL for the logo so it renders directly as a web image in the email header
    without attaching any file to the email.
    """
    custom_logo_url = getattr(settings, "LOGO_URL", "") or ""
    if custom_logo_url:
        return custom_logo_url

    if request is not None:
        try:
            return request.build_absolute_uri(static("tabler/img/logo.png"))
        except Exception:
            pass

    site_url = getattr(settings, "SITE_URL", "") or ""
    if site_url:
        return f"{site_url.rstrip('/')}/static/tabler/img/logo.png"

    return "/static/tabler/img/logo.png"


def send_order_customer_email(order, request=None):
    """
    Sends order confirmation email with logo in header and zero attachments.
    """
    try:
        if not order.email:
            logger.warning("Customer order email skipped: order %s has no email address", order.order_number)
            return False

        subject = f"Order Confirmation #{order.order_number} - Mint Grow"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [order.email]

        context = {
            "order": order,
            "admin_email": settings.ADMIN_EMAIL or settings.DEFAULT_FROM_EMAIL,
            "logo_url": get_logo_url(request),
        }

        text_content = render_to_string("orders/emails/order_customer.txt", context)
        html_content = render_to_string("orders/emails/order_customer.html", context)

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=to_email,
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
        logger.info("Order confirmation email sent to customer %s for order %s", order.email, order.order_number)
        return True
    except Exception as exc:
        logger.error(
            "Failed to send customer order confirmation email for order %s: %s",
            order.order_number,
            exc,
            exc_info=True,
        )
        return False


def send_order_admin_email(order, request=None):
    """
    Sends new order alert email with logo in header and zero attachments.
    """
    try:
        admin_email = getattr(settings, "ADMIN_EMAIL", None) or getattr(settings, "DEFAULT_FROM_EMAIL", None)
        if not admin_email:
            logger.warning("Admin order email skipped: ADMIN_EMAIL is not configured")
            return False

        subject = f"🔔 New Order #{order.order_number} received (₹{order.total_amount})"
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [admin_email]

        admin_order_url = None
        if request is not None:
            try:
                admin_order_url = request.build_absolute_uri(
                    reverse("admin_order_detail", kwargs={"order_id": order.id})
                )
            except Exception:
                admin_order_url = None

        context = {
            "order": order,
            "admin_email": admin_email,
            "admin_order_url": admin_order_url,
            "logo_url": get_logo_url(request),
        }

        text_content = render_to_string("orders/emails/order_admin.txt", context)
        html_content = render_to_string("orders/emails/order_admin.html", context)

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=to_email,
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
        logger.info("Admin order notification email sent to %s for order %s", admin_email, order.order_number)
        return True
    except Exception as exc:
        logger.error(
            "Failed to send admin order notification email for order %s: %s",
            order.order_number,
            exc,
            exc_info=True,
        )
        return False


def send_order_confirmation_emails(order, request=None):
    """
    Dispatches order notification emails to both customer and admin.
    """
    customer_sent = send_order_customer_email(order, request=request)
    admin_sent = send_order_admin_email(order, request=request)
    return customer_sent, admin_sent
