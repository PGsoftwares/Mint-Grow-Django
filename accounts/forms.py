from django import forms
from .models import User
from django.contrib.auth import authenticate


class RegisterForm(forms.ModelForm):
    
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'Password'
            }
        )
    )
    
    confirm_password = forms.CharField(
        widget= forms.PasswordInput(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'Confirm Password'
            }
        )
    )
    
    class Meta:
        
        model = User
        fields = ['name', 'email', 'phone', 'profile_image']
        
        widgets = {
            'email' : forms.EmailInput(
                attrs={
                    'class' : 'form-control',
                    'placeholder' : 'Email'
                }
            ),
            'name' : forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'placeholder' : 'Name'
                }
            ),
            'phone' : forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'placeholder' : 'Phone'
                }
            ),
            'profile_image' : forms.FileInput(
                attrs={
                    'class' : 'form-control'
                }
            )
        }
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Email already exist!')
        
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Password does not match!')
        
        return cleaned_data
    
    def save(self, commit = True):
        user = super().save(commit=False)
        user.role = 'customer'
        user.status = 'active'
        user.is_active = True
        user.set_password(self.cleaned_data['password'])
        
        if commit:
            user.save()
            
        return user
    
class LoginForm(forms.Form):
    
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'Email',
                "autocomplete": "email",
                "autofocus": True,
            }
        )
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'Password',
                "autocomplete": "current-password",
            }
        )
    )
    
    def clean(self):
        cleaned_data = super().clean()
        
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        
        if not email or not password:
            return cleaned_data
        
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise forms.ValidationError('Email / Password does not match!')
        
        if not user.check_password(password):
            raise forms.ValidationError('Email / Password does not match!')    
        
        if user.status != 'active' or not user.is_active:
            raise forms.ValidationError('Your account is inactive!')  
            
        cleaned_data['user'] = user
        
        return cleaned_data
    
    def get_user(self):
        return self.cleaned_data.get('user')
    
    
    
class AdminUserCreateForm(forms.ModelForm):
    
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Password",
                "autocomplete": "new-password",
            }
        )
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm Password",
                "autocomplete": "new-password",
            }
        )
    )
    
    class Meta:
        
        model = User
        fields = ['email', 'name', 'phone', 'profile_image', 'role', 'status']
        
        widgets = {
            'email' : forms.EmailInput(
                attrs={
                    'class' : 'form-control',
                    'placeholder' : 'Email'
                }
            ),
            'name' : forms.TextInput(
                attrs={
                    'class' : 'form-control',
                    'placeholder' : 'Name'
                }
            ),
            'phone' : forms.NumberInput(
                attrs={
                    'class' : 'form-control',
                    'placeholder' : 'Phone'
                }
            ),
            'profile_image' : forms.FileInput(
                attrs={
                    'class' : 'form-control'
                }
            ),
            'role' : forms.Select(
                attrs={
                    'class' : 'form-select'
                }
            ),
            'status' : forms.Select(
                attrs={
                    'class' : 'form-select'
                }
            ),
        }
        
    def clean_email(self):
        
        email = self.cleaned_data.get('email')
        
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError('Email already exists!')
        
        return email
    
    def clean(self):
        
        cleaned_data = super().clean()
        
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Password does not match!')
        
        return cleaned_data
    
    
    def save(self, commit = True):
        user = super().save(commit=False)
        
        if user.role == 'admin':
            user.status = 'active'
            user.is_active = True
            user.is_staff = True
        else:
            user.status = 'active'
            user.is_active = True
            user.is_staff = False
        
        if commit:
            user.save()
            
        return user
    

class AdminUserUpdateForm(forms.ModelForm):
    
    password = forms.CharField(
        required=False,
        label='New Password',
        help_text='Leave blank to keep the current password.',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "New Password",
                "autocomplete": "new-password",
            }
        )
    )
    
    confirm_password = forms.CharField(
        required=False,
        label='Confirm New Password',
        help_text='Leave blank to keep the current password.',
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "placeholder": "Confirm New Password",
                "autocomplete": "new-password",
            }
        )
    )
    
    class Meta:
        
        model = User
        fields = ['email', 'name', 'phone', 'profile_image', 'role', 'status']
        
        widgets = {
            
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Email",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Name",
                }
            ),
            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Phone",
                }
            ),
            "profile_image": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),
            "role": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }
    
    
    def clean_email(self):
        
        email = self.cleaned_data.get('email')
        
        users = User.objects.filter(email__iexact=email)
        
        if self.instance.pk:
            users = users.exclude(pk=self.instance.pk)
            
        if users.exists():
            raise forms.ValidationError('Email already exists!')
        
        return email
    
    
    def clean(self):
        
        cleaned_data = super().clean()
        
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        
        if password or confirm_password:
            
            if not password:
                raise forms.ValidationError('Password is required')
            
            if not confirm_password:
                raise forms.ValidationError('Confirm Password is required')
            
            if password and confirm_password and password != confirm_password:
                raise forms.ValidationError('Password does not match!')
            
        return cleaned_data
    
    
    def save(self, commit = True):
        
        user =  super().save(commit=False)
        
        password = self.cleaned_data.get('password')
        
        if password:            
            user.set_password(password)
        
        if user.role == 'admin':
            user.status = 'active'
            user.is_active = True
            user.is_staff = True
        else:
            user.status = 'active'
            user.is_active = True
            user.is_staff = False
        
        if commit:
            user.save()
            
        return user
            
        
        
        
        