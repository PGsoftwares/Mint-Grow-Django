from django.shortcuts import redirect

def admin_required(view_func):
    
    def wrapper(request, *args, **kwargs):
        
        if not request.user.is_authenticated:
            return redirect('login')
        
        if request.user.role == 'customer':
            return redirect('customer_dashboard')
        
        if request.user.role == 'admin':
            return view_func(request, *args, **kwargs)
        
        return redirect('login')
    
    return wrapper
        

def customer_required(view_func):
    
    def wrapper(request, *args, **kwargs):
        
        if not request.user.is_authenticated:
            return redirect('login')
        
        if request.user.role == 'admin':
            return redirect('dashboard')
        
        if request.user.role == 'customer':
            return view_func(request, *args, **kwargs)    
        
        return redirect('login')
    
    return wrapper  