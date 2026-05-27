from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput,label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    role = forms.ChoiceField(choices=[('analyst', 'Analyst'), ('admin', 'Admin')])

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists")
        return username

    def clean(self):
        cleaned = super().clean()
        password1 = cleaned.get("password1")
        password2 = cleaned.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned