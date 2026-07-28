from django.urls import path
from . import views

urlpatterns =[
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('my-dashboard/', views.customer_dashboard_view, name='customer_dashboard'),
    
    path('users/', views.user_list_view, name='user_list'),
    path('users/create/', views.user_create_view, name='user_create'),
    path('users/<int:id>/update/', views.user_update_view, name='user_update'),
    path('users/<int:id>/toggle-status/', views.user_toggle_status_view, name='user_toggle_status'),
    path('users/<int:id>/delete/', views.user_delete_view, name='user_delete'),
    
    
]