from django import forms
from .models import Equipment

class EquipementForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['equipmentname','rent','description','image1','image2'] 
