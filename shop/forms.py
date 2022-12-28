import phonenumber_field.formfields
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget, RegionalPhoneNumberWidget

from .models import *

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'sign-in_form-input register', 'placeholder': 'Username'})
    )
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'sign-in_form-input register', 'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'sign-in_form-input register', 'placeholder': 'Last name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'sign-in_form-input register', 'placeholder': 'Email'})
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'sign-in_form-input register', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'sign-in_form-input register', 'placeholder': 'Confirm password'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'sign-in_form-input register', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'sign-in_form-input', 'placeholder': 'Password'})
    )


class ReviewForm(forms.ModelForm):
    rating = [
        (5, 5),
        (4, 4),
        (3, 3),
        (2, 2),
        (1, 1),
    ]

    text = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'review-text form-input', 'placeholder': 'Your Review *'})
    )
    name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'name-input form-input', 'placeholder': 'Your Name *'})
    )
    star_rating = forms.IntegerField(
        widget=forms.RadioSelect(choices=rating),
    )
    user = forms.IntegerField(required=False)
    product = forms.IntegerField(required=False)

    class Meta:
        model = Review
        fields = ('text', 'name', 'star_rating', 'user', 'product')


class OrderForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'billing_input', 'placeholder': 'First name *'})
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'billing_input', 'placeholder': 'Last name *'})
    )
    company_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'billing_input', 'placeholder': 'Company Name'})
    )
    country = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'billing_input', 'placeholder': 'Country *'})
    )
    town = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'billing_input', 'placeholder': 'Town *'})
    )
    street = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'billing_input', 'placeholder': 'Street *'})
    )
    postcode = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'billing_input', 'placeholder': 'Postcode *'})
    )
    phone = phonenumber_field.formfields.PhoneNumberField(widget=forms.TextInput(attrs={'class': 'billing_input', 'placeholder': 'Phone *'}))
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'billing_input', 'placeholder': 'Email *'})
    )
    order_notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'billing_input', 'placeholder': 'Order notes', 'rows': '3'})
    )

    class Meta:
        model = Order
        fields = (
            'sale', 'first_name', 'last_name',
            'company_name', 'country', 'street', 'postcode',
            'town', 'phone', 'email', 'order_notes'
        )


