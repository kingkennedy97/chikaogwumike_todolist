from django import forms
from .models import Task

# The PositionForm Class is used to Reorder Form and View


class PositionForm(forms.ModelForm):
    class Meta:
        position = forms.CharField()

