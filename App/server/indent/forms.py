from django import forms
from django import forms
from django.views.decorators.http import require_http_methods 
from .models import Part

class Order(forms.Form):
    part_id = forms.ModelChoiceField(Part.objects.all().values_list('pk',flat=True),required=True)
    dues_in = forms.IntegerField(required=True)
    dues_out = forms.IntegerField(required=True)

class Part_Entity(forms.Form):
    entity_id = forms.CharField(max_length=40,required=True)
    part_id = forms.ModelChoiceField(Part.objects.all().values_list('pk',flat=True),required=True)
    indent = forms.CharField(max_length=40)
    status = forms.CharField()
    location = forms.CharField()
    maintentance_status = forms.ChoiceField(choices=[('A','A'),('B','B'),('C','C'),('D','D'),('E','E'),('F','F')],required=True)
