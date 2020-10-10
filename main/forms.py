from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)    
    class Meta:
        model = User
        fields = ("username", "email","first_name","last_name","password1", "password2")


    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
        return user

class EditProfileForm(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields =  (
            'username',
            'email',
            'first_name',
            'last_name',
        )
        labels = {
            'username': _('Nama Pengguna'),
            'email': _('Email'),
            'first_name': _('Nama Depan'),
            'last_name': _('Nama Belakang')
        }
        help_texts = {
            'username': _('Diperlukan. 150 karakter atau kurang. Hanya huruf, angka, dan @/./+/-/_ saja.'),
        }


              