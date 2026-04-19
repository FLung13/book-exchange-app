from django import forms
from django.forms import ModelForm
from .models import Book

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ["name", "web", "price", "picture", "category"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g., Pride and Prejudice"
            }),
            "web": forms.URLInput(attrs={
                "class": "form-control",
                "placeholder": "https://..."
            }),
            "price": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "19.99",
                "step": "0.01",
                "min": "0"
            }),
            "picture": forms.ClearableFileInput(attrs={
                "class": "form-control"
            }),
            "category": forms.Select(attrs={"class": "form-select"}),
        }
