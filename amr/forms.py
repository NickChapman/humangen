from django import forms


class UserRegistrationForm(forms.Form):
    email = forms.EmailField(label="Your email")
    confirm_email = forms.EmailField(label="Confirm your email")
    password = forms.CharField(label="Set password", max_length=100, widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm password", max_length=100, widget=forms.PasswordInput)


class UserLoginForm(forms.Form):
    email = forms.EmailField(label="Your email")
    password = forms.CharField(label="Your password", max_length=100, widget=forms.PasswordInput)


class AmrGenerationForm(forms.Form):
    amr_id = forms.IntegerField(widget=forms.HiddenInput)
    generation = forms.CharField(max_length=1000, widget=forms.Textarea)