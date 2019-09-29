from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()
class signup(forms.Form):
    username = forms.CharField(max_length=50)
    mail = forms.EmailField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())
    cnf_password = forms.CharField(widget=forms.PasswordInput())
class signin(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())
class PasswordChangeForm(forms.Form):
    name = forms.CharField(max_length=50)