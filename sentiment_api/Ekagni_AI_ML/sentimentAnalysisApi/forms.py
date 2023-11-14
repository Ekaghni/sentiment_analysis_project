from django import forms
from .models import TempImage,Monitor

class TempImageForm(forms.ModelForm) :
   class Meta :
      model = TempImage
      fields = '__all__'

class MonitoringForm(forms.ModelForm):
   class Meta :
      model = Monitor
      fields = '__all__'