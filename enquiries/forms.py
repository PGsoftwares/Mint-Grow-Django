from django import forms

from .models import ProductEnquiry


class ProductEnquiryForm(forms.ModelForm):

    class Meta:
        model = ProductEnquiry

        fields = [
            "name",
            "email",
            "phone",
            "variation",
            "quantity",
            "message",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your name",
                }
            ),

            "email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your email address",
                }
            ),

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Your phone number",
                }
            ),

            "variation": forms.Select(
                attrs={
                    "class": "form-control",
                }
            ),

            "quantity": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter quantity",
                    "min": "1",
                    "step": "0.01",
                }
            ),

            "message": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Tell us what you need...",
                    "rows": 5,
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        product = kwargs.pop("product", None)

        super().__init__(*args, **kwargs)

        if product:
            self.fields["variation"].queryset = (
                product.price_variations.all()
            )

        self.fields["variation"].required = False
        self.fields["quantity"].required = False
        self.fields["message"].required = False