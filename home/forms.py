from django import forms
from .models import HeroSlider


class HeroSliderForm(forms.ModelForm):

    class Meta:
        model = HeroSlider

        fields = [
            "label",
            "title",
            "highlight_text",
            "description",
            "button1_text",
            "button1_url",
            "button2_text",
            "button2_url",
            "image",
            "mobile_image",
            "sort_order",
            "status",
        ]

        widgets = {

            "label": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: 🌱 Farmer-led integrated food company",
                }
            ),

            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: Fresh produce from",
                }
            ),

            "highlight_text": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: farm to future.",
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Enter slider description...",
                }
            ),

            "button1_text": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: View Our Products",
                }
            ),

            "button1_url": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: #products",
                }
            ),

            "button2_text": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: Discover Our Story",
                }
            ),

            "button2_url": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Example: /about/",
                }
            ),

            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),

            "mobile_image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),

            "sort_order": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": 0,
                }
            ),

            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }