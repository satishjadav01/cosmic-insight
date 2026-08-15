from django import forms
from sets.models import NumerologyId

class BirthdateFrom(forms.ModelForm):
    class Meta:
        model = NumerologyId
        fields = ['birth_date']
        widgets = {
            'birth_date':forms.DateInput(attrs={'type':'date'})
        }