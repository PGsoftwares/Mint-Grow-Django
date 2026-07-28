from pathlib import Path

from django import forms
from django.core.exceptions import ValidationError

from .models import Product


class ProductForm(forms.ModelForm):

    ALLOWED_IMAGE_EXTENSIONS = [
        ".jpg",
        ".jpeg",
        ".png",
        ".webp",
    ]

    MAX_IMAGE_SIZE = 2 * 1024 * 1024  # 2 MB

    class Meta:

        model = Product

        fields = [
            "category",
            "name",
            "short_description",
            "description",
            "image",
            "sku",
            "price",
            "featured",
            "status",
        ]

        widgets = {
            "category": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter product name",
                }
            ),
            "short_description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter a short product description",
                    "rows": 3,
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter the full product description",
                    "rows": 6,
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".jpg,.jpeg,.png,.webp",
                }
            ),
            "sku": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter product SKU",
                }
            ),
            "price": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "0.00",
                    "min": "0",
                    "step": "0.01",
                }
            ),
            "featured": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }

    def clean_name(self):

        name = self.cleaned_data.get("name", "").strip()

        if not name:
            raise ValidationError("Product name is required.")

        return name

    def clean_category(self):

        category = self.cleaned_data.get("category")

        if not category:
            raise ValidationError("Please select a category.")

        return category

    def clean_sku(self):

        sku = self.cleaned_data.get("sku", "").strip()

        if not sku:
            raise ValidationError("SKU is required.")

        products = Product.objects.filter(sku__iexact=sku)

        if self.instance.pk:
            products = products.exclude(pk=self.instance.pk)

        if products.exists():
            raise ValidationError(
                "A product with this SKU already exists."
            )

        return sku

    def clean_price(self):

        price = self.cleaned_data.get("price")

        if price is None:
            raise ValidationError("Price is required.")

        if price < 0:
            raise ValidationError(
                "Price must be greater than or equal to zero."
            )

        return price

    def clean_image(self):

        image = self.cleaned_data.get("image")

        if not image:
            return image

        # Skip validation when it is the existing saved image.
        if not hasattr(image, "content_type"):
            return image

        extension = Path(image.name).suffix.lower()

        if extension not in self.ALLOWED_IMAGE_EXTENSIONS:
            raise ValidationError(
                "Only JPG, JPEG, PNG and WEBP images are allowed."
            )

        if image.size > self.MAX_IMAGE_SIZE:
            raise ValidationError(
                "Image size must not exceed 2 MB."
            )

        allowed_content_types = [
            "image/jpeg",
            "image/png",
            "image/webp",
        ]

        if image.content_type not in allowed_content_types:
            raise ValidationError(
                "The uploaded file must be a valid image."
            )

        return image