# products/urls.py

from django.urls import path

from . import views


urlpatterns = [
    
    # Public pages
    path(
        "all/",
        views.public_product_list_view,
        name="public_product_list",
    ),

    path(
        "detail/<slug:slug>/",
        views.public_product_detail_view,
        name="public_product_detail",
    ),
    
    path(
        "",
        views.product_list_view,
        name="product_list",
    ),

    path(
        "create/",
        views.product_create_view,
        name="product_create",
    ),

    path(
        "<int:id>/update/",
        views.product_update_view,
        name="product_update",
    ),

    path(
        "<int:id>/toggle-status/",
        views.product_toggle_status_view,
        name="product_toggle_status",
    ),

    path(
        "<int:id>/delete/",
        views.product_delete_view,
        name="product_delete",
    ),
    
    # Public Excel download
    path(
        "download-price-list/",
        views.download_price_list_view,
        name="download_price_list",
    ),
]