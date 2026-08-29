from decimal import Decimal
import razorpay
from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.views.decorators.http import require_POST

from products.models import Product, ProductPriceVariation

from .cart import Cart
from .forms import CheckoutForm
from .models import Order, OrderItem
from django.core.paginator import Paginator
from django.db.models import Q
from accounts.decorators import admin_required


@require_POST
def cart_add(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id,
        status="active",
    )

    variation_id = request.POST.get(
        "variation_id"
    )

    quantity = request.POST.get(
        "quantity",
        1,
    )

    try:
        quantity = int(quantity)

    except (TypeError, ValueError):
        quantity = 1

    if quantity < 1:
        quantity = 1

    variation = get_object_or_404(
        ProductPriceVariation,
        id=variation_id,
        product=product,
    )

    if variation.stock <= 0:

        messages.error(
            request,
            (
                f"{product.name} - "
                f"{variation.name} is out of stock."
            ),
        )

        return redirect(
            "cart_detail"
        )

    cart = Cart(request)

    cart_key = str(
        variation.id
    )

    existing_quantity = 0

    if cart_key in cart.cart:
        existing_quantity = cart.cart[
            cart_key
        ]["quantity"]

    requested_total = (
        existing_quantity + quantity
    )

    if requested_total > variation.stock:

        messages.error(
            request,
            (
                f"Only "
                f"{variation.stock.normalize()} "
                f"{variation.get_stock_unit_display()} "
                f"available for "
                f"{product.name} - "
                f"{variation.name}."
            ),
        )

        return redirect(
            "cart_detail"
        )

    cart.add(
        product=product,
        variation=variation,
        quantity=quantity,
    )

    messages.success(
        request,
        f"{product.name} added to cart.",
    )

    return redirect(
        "cart_detail"
    )


def cart_detail(request):

    cart = Cart(request)

    cart_items = []

    total = Decimal("0.00")

    for item in cart.cart.values():

        product = Product.objects.filter(
            id=item["product_id"]
        ).first()
        
        variation = ProductPriceVariation.objects.filter(
            id=item["variation_id"],
            product=product,
        ).first()

        if not product or not variation:
            continue

        price = Decimal(
            item["price"]
        )

        quantity = item["quantity"]

        item_total = (
            price * quantity
        )

        total += item_total

        cart_items.append(
            {
                "product": product,
                "variation": variation,
                "price": price,
                "quantity": quantity,
                "total": item_total,
            }
        )

    context = {
        "cart_items": cart_items,
        "cart_total": total,
    }

    return render(
        request,
        "orders/cart.html",
        context,
    )


@require_POST
def cart_update(request, variation_id):

    cart = Cart(request)

    variation = get_object_or_404(
        ProductPriceVariation,
        id=variation_id,
    )

    quantity = request.POST.get(
        "quantity",
        1,
    )

    try:
        quantity = int(quantity)

    except (TypeError, ValueError):
        quantity = 1

    cart_key = str(
        variation_id
    )

    if cart_key not in cart.cart:
        return redirect(
            "cart_detail"
        )

    if quantity <= 0:

        cart.remove(
            variation_id
        )

        return redirect(
            "cart_detail"
        )

    # Check available stock
    if quantity > variation.stock:

        messages.error(
            request,
            (
                f"Only "
                f"{variation.stock.normalize()} "
                f"{variation.get_stock_unit_display()} "
                f"available for "
                f"{variation.product.name} - "
                f"{variation.name}."
            ),
        )

        return redirect(
            "cart_detail"
        )

    cart.cart[
        cart_key
    ]["quantity"] = quantity

    cart.save()

    messages.success(
        request,
        "Cart updated successfully.",
    )

    return redirect(
        "cart_detail"
    )


@require_POST
def cart_remove(request, variation_id):

    cart = Cart(request)

    cart.remove(
        variation_id
    )

    messages.success(
        request,
        "Product removed from cart."
    )

    return redirect(
        "cart_detail"
    )


def checkout(request):

    cart = Cart(request)

    if not cart.cart:

        messages.error(
            request,
            "Your cart is empty.",
        )

        return redirect(
            "public_product_list"
        )

    cart_items = []

    total = Decimal("0.00")

    for item in cart.cart.values():

        product = Product.objects.filter(
            id=item["product_id"],
            status="active",
        ).first()

        if not product:
            continue

        variation = ProductPriceVariation.objects.filter(
            id=item["variation_id"],
            product=product,
        ).first()

        if not variation:
            continue

        price = variation.price

        quantity = item["quantity"]

        item_total = price * quantity

        total += item_total

        cart_items.append(
            {
                "product": product,
                "variation": variation,
                "price": price,
                "quantity": quantity,
                "total": item_total,
            }
        )

    if not cart_items:

        messages.error(
            request,
            "Your cart does not contain valid products.",
        )

        return redirect(
            "public_product_list"
        )

    if request.method == "POST":

        form = CheckoutForm(
            request.POST
        )

        if form.is_valid():

            try:

                with transaction.atomic():

                    locked_items = []

                    total = Decimal("0.00")

                    # Re-check and lock stock
                    for item in cart_items:

                        variation = (
                            ProductPriceVariation.objects
                            .select_for_update()
                            .get(
                                id=item["variation"].id
                            )
                        )

                        quantity = item["quantity"]

                        if variation.stock <= 0:

                            raise ValueError(
                                (
                                    f"{variation.product.name} - "
                                    f"{variation.name} "
                                    f"is out of stock."
                                )
                            )

                        if quantity > variation.stock:

                            raise ValueError(
                                (
                                    f"Only "
                                    f"{variation.stock.normalize()} "
                                    f"{variation.get_stock_unit_display()} "
                                    f"available for "
                                    f"{variation.product.name} - "
                                    f"{variation.name}."
                                )
                            )

                        price = variation.price

                        item_total = (
                            price * quantity
                        )

                        total += item_total

                        locked_items.append(
                            {
                                "product": variation.product,
                                "variation": variation,
                                "price": price,
                                "quantity": quantity,
                                "total": item_total,
                            }
                        )

                    # Create Django order
                    order = form.save(
                        commit=False
                    )

                    order.total_amount = total

                    order.payment_status = "pending"

                    order.save()

                    # Create order items
                    for item in locked_items:

                        OrderItem.objects.create(
                            order=order,
                            product=item["product"],
                            variation=item["variation"],
                            product_name=item["product"].name,
                            variation_name=item["variation"].name,
                            unit=item["variation"].stock_unit,
                            price=item["price"],
                            quantity=item["quantity"],
                            total=item["total"],
                        )

                # --------------------------------
                # CASH ON DELIVERY
                # --------------------------------

                if order.payment_method == "cod":

                    for item in locked_items:

                        variation = item["variation"]

                        variation.stock -= item["quantity"]

                        variation.save(
                            update_fields=[
                                "stock",
                                "updated_at",
                            ]
                        )

                    order.payment_status = "pending"

                    order.save(
                        update_fields=[
                            "payment_status",
                            "updated_at",
                        ]
                    )

                    cart.clear()

                    messages.success(
                        request,
                        "Order placed successfully.",
                    )

                    return redirect(
                        "order_success",
                        order_number=order.order_number,
                    )

                # --------------------------------
                # RAZORPAY
                # --------------------------------

                if order.payment_method == "razorpay":

                    client = razorpay.Client(
                        auth=(
                            settings.RAZORPAY_KEY_ID,
                            settings.RAZORPAY_KEY_SECRET,
                        )
                    )

                    razorpay_order = client.order.create(
                        {
                            "amount": int(
                                total * Decimal("100")
                            ),
                            "currency": "INR",
                            "receipt": order.order_number,
                        }
                    )

                    order.razorpay_order_id = (
                        razorpay_order["id"]
                    )

                    order.save(
                        update_fields=[
                            "razorpay_order_id",
                            "updated_at",
                        ]
                    )

                    context = {
                        "order": order,
                        "razorpay_order_id": razorpay_order["id"],
                        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
                        "amount": int(
                            total * Decimal("100")
                        ),
                        "currency": "INR",
                    }

                    return render(
                        request,
                        "orders/payment.html",
                        context,
                    )

            except ValueError as error:

                messages.error(
                    request,
                    str(error),
                )

                return redirect(
                    "cart_detail"
                )

            except Exception as error:

                messages.error(
                    request,
                    (
                        "Unable to create payment. "
                        "Please try again."
                    ),
                )

                return redirect(
                    "checkout"
                )

    else:

        initial = {}

        if request.user.is_authenticated:

            initial = {
                "name": request.user.name,
                "email": request.user.email,
                "phone": request.user.phone,
            }

        form = CheckoutForm(
            initial=initial
        )

    context = {
        "form": form,
        "cart_items": cart_items,
        "cart_total": total,
    }

    return render(
        request,
        "orders/checkout.html",
        context,
    )

@require_POST
def razorpay_payment_success(request):

    razorpay_payment_id = request.POST.get(
        "razorpay_payment_id"
    )

    razorpay_order_id = request.POST.get(
        "razorpay_order_id"
    )

    razorpay_signature = request.POST.get(
        "razorpay_signature"
    )

    if not all(
        [
            razorpay_payment_id,
            razorpay_order_id,
            razorpay_signature,
        ]
    ):

        messages.error(
            request,
            "Invalid payment response.",
        )

        return redirect(
            "public_product_list"
        )

    order = get_object_or_404(
        Order,
        razorpay_order_id=razorpay_order_id,
    )

    # Already paid
    if order.payment_status == "paid":

        return redirect(
            "order_success",
            order_number=order.order_number,
        )

    client = razorpay.Client(
        auth=(
            settings.RAZORPAY_KEY_ID,
            settings.RAZORPAY_KEY_SECRET,
        )
    )

    try:

        # Verify Razorpay payment signature
        client.utility.verify_payment_signature(
            {
                "razorpay_order_id": razorpay_order_id,
                "razorpay_payment_id": razorpay_payment_id,
                "razorpay_signature": razorpay_signature,
            }
        )

    except razorpay.errors.SignatureVerificationError:

        order.payment_status = "failed"

        order.save(
            update_fields=[
                "payment_status",
                "updated_at",
            ]
        )

        messages.error(
            request,
            "Payment verification failed.",
        )

        return redirect(
            "checkout"
        )

    # --------------------------------
    # Payment verified successfully
    # --------------------------------

    try:

        with transaction.atomic():

            locked_order = (
                Order.objects
                .select_for_update()
                .get(
                    id=order.id
                )
            )

            # Prevent duplicate processing
            if locked_order.payment_status == "paid":

                return redirect(
                    "order_success",
                    order_number=locked_order.order_number,
                )

            # Get order items
            order_items = (
                OrderItem.objects
                .filter(
                    order=locked_order
                )
            )

            # Lock all product variations and check/reduce stock
            for item in order_items:

                variation = (
                    ProductPriceVariation.objects
                    .select_for_update()
                    .get(
                        id=item.variation_id
                    )
                )

                if variation.stock <= 0:

                    raise ValueError(
                        (
                            f"{item.product_name} - "
                            f"{item.variation_name} "
                            f"is no longer available."
                        )
                    )

                if item.quantity > variation.stock:

                    raise ValueError(
                        (
                            f"Insufficient stock for "
                            f"{item.product_name} - "
                            f"{item.variation_name}."
                        )
                    )

                variation.stock -= item.quantity

                variation.save(
                    update_fields=[
                        "stock",
                        "updated_at",
                    ]
                )

            # Save payment details
            locked_order.razorpay_payment_id = (
                razorpay_payment_id
            )

            locked_order.razorpay_signature = (
                razorpay_signature
            )

            locked_order.payment_status = "paid"

            locked_order.save(
                update_fields=[
                    "razorpay_payment_id",
                    "razorpay_signature",
                    "payment_status",
                    "updated_at",
                ]
            )

        # Clear cart only after successful payment
        cart = Cart(request)

        cart.clear()

        messages.success(
            request,
            "Payment successful. Your order has been placed.",
        )

        return redirect(
            "order_success",
            order_number=locked_order.order_number,
        )

    except ValueError as error:

        messages.error(
            request,
            str(error),
        )

        return redirect(
            "checkout"
        )
        
        
def order_success(
    request,
    order_number,
):

    return render(
        request,
        "orders/success.html",
        {
            "order_number": order_number,
        },
    )
def order_failed(
    request,
    order_number,
):

    return render(
        request,
        "orders/failed.html",
        {
            "order_number": order_number,
        },
    )
    
@require_POST
def razorpay_payment_cancel(request):

    order_number = request.POST.get(
        "order_number"
    )

    if order_number:
        # Delete pending order if user cancelled / closed the checkout modal
        Order.objects.filter(
            order_number=order_number,
            payment_method="razorpay",
            payment_status="pending",
        ).delete()

    messages.info(
        request,
        "Payment was cancelled. You can retry or choose another payment method.",
    )

    return redirect(
        "checkout"
    )

@require_POST
def razorpay_payment_failed(request):

    order_number = request.POST.get(
        "order_number"
    )

    if order_number:

        order = Order.objects.filter(
            order_number=order_number
        ).first()

        if order:

            order.payment_status = "failed"

            order.save(
                update_fields=[
                    "payment_status",
                    "updated_at",
                ]
            )

    return redirect(
        "order_failed",
        order_number=order_number or "unknown",
    )
    
@admin_required
def admin_order_list(request):
    orders = (
        Order.objects
        .exclude(
            payment_method="razorpay",
            payment_status="pending",
        )
        .prefetch_related("items")
        .order_by("-created_at")
    )

    search = request.GET.get(
        "search",
        "",
    ).strip()

    status = request.GET.get(
        "status",
        "",
    ).strip()

    if search:
        orders = orders.filter(
            Q(order_number__icontains=search)
            | Q(name__icontains=search)
            | Q(email__icontains=search)
            | Q(phone__icontains=search)
        )

    if status:
        orders = orders.filter(
            status=status
        )

    paginator = Paginator(
        orders,
        10,
    )

    page_number = request.GET.get(
        "page"
    )

    page_obj = paginator.get_page(
        page_number
    )

    context = {
        "orders": page_obj,
        "page_obj": page_obj,
        "search": search,
        "selected_status": status,
        "status_choices": Order.STATUS_CHOICES,
    }

    return render(
        request,
        "orders/admin/list.html",
        context,
    )


@admin_required
def admin_order_detail(
    request,
    order_id,
):
    order = get_object_or_404(
        Order.objects.prefetch_related(
            "items__product"
        ),
        id=order_id,
    )

    context = {
        "order": order,
        "status_choices": Order.STATUS_CHOICES,
    }

    return render(
        request,
        "orders/admin/detail.html",
        context,
    )


@require_POST
@admin_required
def admin_order_status_update(
    request,
    order_id,
):
    order = get_object_or_404(
        Order,
        id=order_id,
    )

    status = request.POST.get(
        "status"
    )

    valid_statuses = [
        value
        for value, label
        in Order.STATUS_CHOICES
    ]

    if status not in valid_statuses:
        messages.error(
            request,
            "Invalid order status.",
        )

        return redirect(
            "admin_order_detail",
            order_id=order.id,
        )

    order.status = status

    order.save(
        update_fields=[
            "status",
            "updated_at",
        ]
    )

    messages.success(
        request,
        f"Order {order.order_number} updated to {order.get_status_display()}.",
    )

    return redirect(
        "admin_order_detail",
        order_id=order.id,
    )