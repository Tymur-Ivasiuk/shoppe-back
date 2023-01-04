import phonenumber_field.formfields
from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordChangeForm, \
    PasswordResetForm, SetPasswordForm
from django.forms import Widget
from django.forms.utils import flatatt
from django.utils.html import format_html

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


class UpdateUserForm(UserChangeForm):
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'sign-in_form-input register', 'placeholder': 'First name'})
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'sign-in_form-input register', 'placeholder': 'Last name'})
    )
    email = forms.CharField(
        required=False,
        widget=forms.EmailInput(attrs={'class': 'sign-in_form-input register', 'placeholder': 'Email'})
    )
    username = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'sign-in_form-input register', 'placeholder': 'Username'})
    )
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')


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

class ResetPasswordEmail(PasswordResetForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Email'})
    )

class SetPassword(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'New password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Confirm password'}),
    )


class ContactForm(forms.Form):
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'contact-form_text', 'placeholder': 'First name *'})
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'contact-form_text', 'placeholder': 'Last name *'})
    )
    subject = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'contact-form_text', 'placeholder': 'Subject *'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'contact-form_text', 'placeholder': 'Email *'})
    )
    message = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'contact-form_text', 'rows': '3', 'style': 'resize: none;', 'placeholder': 'Message'})
    )

class OrderListFormAdmin(forms.ModelForm):
    new_quantity = forms.IntegerField(required=False)
    quantity = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'readonly': 'true'})
    )

    class Meta:
        model = OrderList
        exclude = ('', )
