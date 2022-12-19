from django import forms
from .models import *

class CheckForm(forms.Form):
    title = forms.BooleanField()