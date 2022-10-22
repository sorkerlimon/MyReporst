
from dataclasses import fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from django import forms

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length = 200, required=True, label="Email Address")
    class Meta:
        model = User
        fields = ['email','first_name','password1','password2']
        labels = {
            'first_name':'Full Name',
            }
    
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm,self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

             
            
class DateInput(forms.DateInput):
    input_type = 'date'


class ProfleForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name','username','email','location','gender','blood','phone_number','dob','profile_image']
        exclude = ['username']
        labels = {
            'dob':'Birth Date'
            }
        widgets = {'dob': DateInput()}
        
        
    def __init__(self, *args, **kwargs):
        super(ProfleForm,self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})