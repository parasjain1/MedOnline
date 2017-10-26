from django import forms
from django.forms import ModelForm
from models import Patient, Doctor
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class LoginForm(forms.Form):
    email = forms.CharField(label='Email', max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    password = forms.CharField(label='Password', max_length=100, widget= forms.PasswordInput(attrs={'class' : 'form-control'}))
    def clean(self):
        username = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError("Invalid email or password!")
        elif not user.is_active:
            raise forms.ValidationError("User account deactivated. Please mail us if this concerns you.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


class RegisterForm(forms.Form):
    BIRTH_YEAR_CHOICES = range(1950,datetime.now().year)
    USER_TYPE_CHOICES = {('1','Patient'), ('2','Doctor')}
    firstName = forms.CharField(label='First Name', max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    lastName = forms.CharField(label='Last Name', max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    contact = forms.CharField(label='Contact', max_length=10, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    line1 = forms.CharField(label='Address Line 1', max_length=200, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    line2 = forms.CharField(label='Address Line 2', max_length=200, required=False, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    pinCode = forms.CharField(label='Pincode', max_length=10, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    city = forms.CharField(label='City', max_length=30, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    state = forms.CharField(label='State', max_length=30, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    date = forms.DateField(label='DOB', widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES))
    email = forms.CharField(label='Email', max_length=100, widget=forms.TextInput(attrs={'class' : 'form-control'}))
    password = forms.CharField(label='Password', max_length=100, widget= forms.PasswordInput(attrs={'class' : 'form-control'}))
    type = forms.ChoiceField(label='Doctor or Patient', widget=forms.RadioSelect, choices=USER_TYPE_CHOICES)
    doctor = forms.ModelChoiceField(label='Choose your Doctor', queryset=Doctor.objects.all(), required=False)


    def clean(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
             msg = (u'Duplicate Error!')
             self._errors['email'] = self.error_class([msg])
             del self.cleaned_data['email']
        return self.cleaned_data


class UploadProfileImageForm(forms.Form):
    file = forms.FileField()
