from django import forms


class UserRegistrationForm(forms.Form):
    email = forms.EmailField(label="Your email")
    password = forms.PasswordInput(label="Set password")
    confirm_password = forms.PasswordInput(label="Confirm password")
