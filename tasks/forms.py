from django import forms


class LoginForm(forms.Form):
    Username = forms.CharField(widget=forms.TextInput)
    Password = forms.CharField(widget=forms.PasswordInput)

    
