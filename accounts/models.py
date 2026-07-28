from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, name, phone, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        if not name:
            raise ValueError("Name is required")

        if not phone:
            raise ValueError("Phone is required")

        email = self.normalize_email(email).lower()

        extra_fields.setdefault("role", "customer")
        extra_fields.setdefault("status", "active")
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user = self.model(
            email=email, 
            name=name, 
            phone=phone, 
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, phone, password=None, **extra_fields):
        extra_fields["role"] = "admin"
        extra_fields["status"] = "active"
        extra_fields["is_active"] = True
        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(
            email=email,
            name=name,
            phone=phone,
            password=password,
            **extra_fields,
        )


class User(AbstractBaseUser, PermissionsMixin):
    
    username = None
    first_name = None
    last_name = None
    
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("customer", "Customer"),
    )

    STATUS_CHOICES = (
        ("active", "Active"),
        ("inactive", "Inactive"),
    )

    email = models.EmailField(max_length=255, unique=True)

    name = models.CharField(max_length=255)

    phone = models.CharField(max_length=15, unique=True)

    profile_image = models.ImageField(
        upload_to="profile_images/",
        blank=True,
        null=True,
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="customer")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["name", "phone"]

    objects = UserManager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.email

