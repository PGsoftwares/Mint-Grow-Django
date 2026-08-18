from django.urls import path
from . import views
urlpatterns = [
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    
    path(
        "admin/hero-sliders/",
        views.admin_hero_slider_list_view,
        name="admin_hero_slider_list",
    ),

    path(
        "admin/hero-sliders/add/",
        views.admin_hero_slider_create_view,
        name="admin_hero_slider_create",
    ),

    path(
        "admin/hero-sliders/<int:pk>/edit/",
        views.admin_hero_slider_edit_view,
        name="admin_hero_slider_edit",
    ),

    path(
        "admin/hero-sliders/<int:pk>/delete/",
        views.admin_hero_slider_delete_view,
        name="admin_hero_slider_delete",
    ),
]