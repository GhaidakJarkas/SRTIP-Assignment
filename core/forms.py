from django import forms
from core.models import Customer


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['name', 'email', 'mobile', 'dob', 'address', 'emirate', 'country', 'city']