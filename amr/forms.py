from django import forms


class UserRegistrationForm(forms.Form):
    email = forms.EmailField(label="Your email")
    password = forms.CharField(label="Set password", max_length=100, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm password", max_length=100, widget=forms.PasswordInput)
