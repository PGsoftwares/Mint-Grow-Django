from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages

from .forms import RegisterForm, LoginForm, AdminUserCreateForm, AdminUserUpdateForm
from .models import User
from .decorators import admin_required, customer_required

from django.views.decorators.http import require_POST

from categories.models import ProductCategory
from products.models import Product

def register_view(request):
    
    if request.user.is_authenticated:        
        if request.user.role == 'admin':
            return redirect('dashboard')
        return redirect('customer_dashboard')
    
    form = RegisterForm(request.POST or None, request.FILES or None)
    
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Register successful')
            return redirect('login')
        messages.error(request, 'Please fill all the fileds!')
    
    return render(request, 'accounts/register.html', {'form':form})


def login_view(request):
    
    if request.user.is_authenticated:
        if request.user.role == 'admin':
            return redirect('dashboard')
        return redirect('customer_dashboard')
    
    form = LoginForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Login successful!')
            
            if user.role == 'admin':
                return redirect('dashboard')
            
            return redirect('customer_dashboard')
        messages.error(request,'Invalid credentials!')
    
    return render(request, 'accounts/login.html',{'form':form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out!')
    return redirect('login')


@admin_required
def dashboard_view(request):
    customers = User.objects.filter(role="customer")

    total_users = User.objects.count()
    total_customers = customers.count()

    active_customers = customers.filter(
        status="active",
        is_active=True,
    ).count()

    inactive_customers = customers.filter(
        status="inactive",
    ).count()

    total_categories = ProductCategory.objects.count()
    total_products = Product.objects.count()

    active_products = Product.objects.filter(
        status="active",
    ).count()

    inactive_products = Product.objects.filter(
        status="inactive",
    ).count()

    featured_products = Product.objects.filter(
        featured=True,
    ).count()

    active_customer_percentage = (
        round(active_customers / total_customers * 100)
        if total_customers
        else 0
    )

    active_product_percentage = (
        round(active_products / total_products * 100)
        if total_products
        else 0
    )

    inactive_product_percentage = (
        round(inactive_products / total_products * 100)
        if total_products
        else 0
    )

    featured_product_percentage = (
        round(featured_products / total_products * 100)
        if total_products
        else 0
    )

    recent_users = User.objects.order_by(
        "-created_at"
    )[:5]

    context = {
        "total_users": total_users,
        "total_customers": total_customers,
        "active_customers": active_customers,
        "inactive_customers": inactive_customers,

        "total_categories": total_categories,
        "total_products": total_products,
        "active_products": active_products,
        "inactive_products": inactive_products,
        "featured_products": featured_products,

        "active_customer_percentage": active_customer_percentage,
        "active_product_percentage": active_product_percentage,
        "inactive_product_percentage": inactive_product_percentage,
        "featured_product_percentage": featured_product_percentage,

        "recent_users": recent_users,
    }

    return render(
        request,
        "accounts/dashboard.html",
        context,
    )


@customer_required
def customer_dashboard_view(request):
    return render(request, 'accounts/customer_dashboard.html')


@admin_required
def user_list_view(request):
    
    users = User.objects.all().order_by('-created_at')       
    return render(request, 'accounts/users/list.html', {'users':users})


@admin_required
def user_create_view(request):
    
    form = AdminUserCreateForm(request.POST or None, request.FILES or None)
    
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            messages.success(f'{user.name} created successfully')
            return redirect('user_list')
        messages.error(request, 'Please correct the errors below.')
    
    return render(request, 'accounts/users/create.html', {'form':form})



@admin_required
def user_update_view(request, id):
    
    user = get_object_or_404(User, id=id)
    
    form = AdminUserUpdateForm(request.POST or None, request.FILES or None, instance=user)
    
    if request.method == 'POST':
        if form.is_valid():
            user.save()
            messages.success(request, f'{user.name} updated successfully!')
            return redirect('user_list')
        messages.error(request, 'Please correct the erros below.')
        
    return render(request, 'accounts/users/edit.html', {'form':form, 'user':user })
    
    
@admin_required
@require_POST
def user_toggle_status_view(request, id):
    
    user = get_object_or_404(User, id=id)
    
    if user == request.user:
        messages.error(request, 'You cannot change your own account status')
        return redirect('user_list')
    
    if user.is_superuser:
        messages.error(request, 'You cannot change superuser account status')
        return redirect('user_list')
    
    if user.status == 'active':
        user.status = 'inactive'
        user.is_active = False
        message = 'User deactivated successfully!'
    
    else:
        user.status = 'active'
        user.is_active = True
        message = 'User activated successfully!'
    
    user.save(
        update_fields=[
            'status',
            'is_active',
            'updated_at'
        ]
    )
    
    messages.success(request, message)
    
    return redirect('user_list')


@admin_required
def user_delete_view(request, id):
    
    user = get_object_or_404(User, id=id)
    
    if user == request.user:
        messages.error(request, 'You cannot delete your own account!')
        return redirect("user_list")
    
    if user.is_superuser:
        messages.error(request, 'You cannot delete supuer user account!')
        return redirect("user_list")
    
    if request.method == 'POST':
        
        if user.profile_image:
            user.profile_image.delete(save=False)
        
        user.delete()
        
        messages.success(request, f'{user.name} deleted successfully!')
        return redirect("user_list")
    
    return render(request, 'accounts/user/delete.html', {'user':user})


        
    