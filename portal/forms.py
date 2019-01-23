from django import forms
from .models import Prospect


class ProspectContactForm(forms.ModelForm):

    class Meta:
        model = Prospect
        fields = ('Phone', 'Email', 'Website', 'Notes')
