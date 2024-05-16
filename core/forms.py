from django import forms
from core.models import Customer, Subscription


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['name', 'email', 'mobile', 'dob', 'address', 'emirate', 'country', 'city']


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['first_name', 'last_name', 'passport_number', 'expiry_date', 'issue_date', 'doc', 'plan']