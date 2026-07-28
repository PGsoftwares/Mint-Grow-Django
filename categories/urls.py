from django.urls import path

from . import views


urlpatterns = [
    
    path(
        "all/",
        views.public_category_list_view,
        name="public_category_list",
    ),
    
    
    path(
        "",
        views.category_list_view,
        name="category_list",
    ),

    path(
        "create/",
        views.category_create_view,
        name="category_create",
    ),

    path(
        "<int:id>/update/",
        views.category_update_view,
        name="category_update",
    ),

    path(
        "<int:id>/toggle-status/",
        views.category_toggle_status_view,
        name="category_toggle_status",
    ),

    path(
        "<int:id>/delete/",
        views.category_delete_view,
        name="category_delete",
    ),
]