from pathlib import Path

from django import forms

from .models import ProductCategory


class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory

        fields = [
            "parent",
            "name",
            "description",
            "image",
            "status",
        ]

        widgets = {
            "parent": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Category name",
                    "autofocus": True,
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Category description",
                    "rows": 4,
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": ".jpg,.jpeg,.png,.webp",
                }
            ),
            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        parent_queryset = ProductCategory.objects.order_by(
            "parent_id",
            "name",
        )

        if self.instance.pk:
            excluded_ids = [
                self.instance.pk,
                *self.get_descendant_ids(self.instance),
            ]

            parent_queryset = parent_queryset.exclude(
                pk__in=excluded_ids,
            )

        self.fields["parent"].queryset = parent_queryset
        self.fields["parent"].required = False
        self.fields["parent"].empty_label = "Main category"

        self.fields["parent"].label_from_instance = (
            lambda category: category.full_name
        )

    def clean_name(self):
        return self.cleaned_data["name"].strip()

    def clean(self):
        cleaned_data = super().clean()

        parent = cleaned_data.get("parent")
        name = cleaned_data.get("name")

        if not name:
            return cleaned_data

        queryset = ProductCategory.objects.filter(
            parent=parent,
            name__iexact=name,
        )

        if self.instance.pk:
            queryset = queryset.exclude(
                pk=self.instance.pk,
            )

        if queryset.exists():
            self.add_error(
                "name",
                "This category already exists under the selected parent.",
            )

        if self.instance.pk and parent:
            if parent.pk == self.instance.pk:
                self.add_error(
                    "parent",
                    "A category cannot be its own parent.",
                )

        return cleaned_data

    def clean_image(self):
        image = self.cleaned_data.get("image")

        if not image:
            return image

        # Existing image during update
        if not hasattr(image, "size"):
            return image

        allowed_extensions = {
            ".jpg",
            ".jpeg",
            ".png",
            ".webp",
        }

        extension = Path(image.name).suffix.lower()

        if extension not in allowed_extensions:
            raise forms.ValidationError(
                "Only JPG, JPEG, PNG and WEBP images are allowed."
            )

        max_size = 2 * 1024 * 1024

        if image.size > max_size:
            raise forms.ValidationError(
                "Image size must not exceed 2 MB."
            )

        return image

    @staticmethod
    def get_descendant_ids(category):
        descendant_ids = []

        for child in category.children.all():
            descendant_ids.append(child.pk)
            descendant_ids.extend(
                ProductCategoryForm.get_descendant_ids(child)
            )

        return descendant_ids