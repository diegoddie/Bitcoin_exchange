from django.contrib.auth.forms import UserCreationForm
from django import forms 
from django.contrib.auth.models import User 
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm
from django.contrib.auth import authenticate

class CustomUserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.EmailField(
        widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

#subclass of AuthenticationForm, which is used for logging in users. It adds the required attribute to the username and password fields, and also adds custom error messages for when these fields are left blank.
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(required=True, error_messages={'required': 'Username is required.'})
    password = forms.CharField(required=True, widget=forms.PasswordInput, error_messages={'required': 'Password is required.'})

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    
    #checks if the email address entered by the user is associated with an existing user account before allowing the form to be submitted.
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Invalid email address.")
        return email          