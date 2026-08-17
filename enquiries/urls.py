from django.urls import path

from .views import (
    enquiry_detail_view,
    enquiry_list_view,
    enquiry_mark_closed_view,
    enquiry_mark_contacted_view,
    product_enquiry_view,
)


urlpatterns = [
    path('enquiry/<slug:slug>/', product_enquiry_view, name='product_enquiry'),
    path("admin/enquiries/", enquiry_list_view, name="enquiry_list"),
    path("admin/enquiries/<int:id>/", enquiry_detail_view, name="enquiry_detail"),
    
    path(
        "admin/enquiries/<int:id>/contacted/",
        enquiry_mark_contacted_view,
        name="enquiry_mark_contacted",
    ),

    path(
        "admin/enquiries/<int:id>/closed/",
        enquiry_mark_closed_view,
        name="enquiry_mark_closed",
    ),
]