from django.urls import path

from . import views


urlpatterns = [

    path(
        "cart/",
        views.cart_detail,
        name="cart_detail",
    ),

    path(
        "cart/add/<int:product_id>/",
        views.cart_add,
        name="cart_add",
    ),

    path(
        "cart/update/<int:variation_id>/",
        views.cart_update,
        name="cart_update",
    ),

    path(
        "cart/remove/<int:variation_id>/",
        views.cart_remove,
        name="cart_remove",
    ),

    path(
        "checkout/",
        views.checkout,
        name="checkout",
    ),

    path(
        "order/success/<str:order_number>/",
        views.order_success,
        name="order_success",
    ),

    path(
        "order/failed/<str:order_number>/",
        views.order_failed,
        name="order_failed",
    ),
    
    # Admin Order Management
    path(
        "admin/orders/",
        views.admin_order_list,
        name="admin_order_list",
    ),

    path(
        "admin/orders/<int:order_id>/",
        views.admin_order_detail,
        name="admin_order_detail",
    ),

    path(
        "admin/orders/<int:order_id>/status/",
        views.admin_order_status_update,
        name="admin_order_status_update",
    ),
    
    path(
        "payment/success/",
        views.razorpay_payment_success,
        name="razorpay_payment_success",
    ),

    path(
        "payment/failed/",
        views.razorpay_payment_failed,
        name="razorpay_payment_failed",
    ),

    path(
        "payment/cancel/",
        views.razorpay_payment_cancel,
        name="razorpay_payment_cancel",
    ),
]