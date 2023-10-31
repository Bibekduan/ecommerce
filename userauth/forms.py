from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauth.models import User,Profile


class UserRegisterForm(UserCreationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username'}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'placeholder':'Email'}))
    password1=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    password2=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'conferm password'}))


    class Meta:
        model=User
        fields=['username','email']



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'image', 'bio', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Full Name'}),
            'bio': forms.TextInput(attrs={'placeholder': 'Bio'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone No'}),
        }
