from django import forms
from django.contrib.auth import authenticate,logout,login

class LoginForm(forms.Form):
    Username = forms.CharField(widget=forms.TextInput)
    Password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('Username')
        password = self.cleaned_data.get('Password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user
