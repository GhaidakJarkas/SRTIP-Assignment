from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from accounts.models import CustomUser


#User Creation Form
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2', 'role']

    def save(self):
        user = super().save(commit=False)
        if self.cleaned_data.get('role') == 'admin':
            user.is_superuser = True
        elif self.cleaned_data.get('role') == 'staff':
            user.is_staff = True
        user.save()
        return user
    

#User Update Form
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'role']

    def save(self):
        user = super().save(commit=False)
        user.is_staff = False
        user.is_superuser = False
        if self.cleaned_data.get('role') == 'admin':
            user.is_superuser = True
        elif self.cleaned_data.get('role') == 'staff':
            user.is_staff = True
        user.save()
        return user