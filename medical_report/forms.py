from django import forms
from .models import Imageadd

class DateInput(forms.DateInput):
    input_type = 'date'

class ImageAddForm(forms.ModelForm):
    
    class Meta:
        model = Imageadd
        fields = ('testdate', 'image')
        labels = {
            'testdate':'Test Date'
            }
        widgets = {'testdate': DateInput()}
        
    def __init__(self, *args, **kwargs):
        super(ImageAddForm,self).__init__(*args, **kwargs)
        
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
    
