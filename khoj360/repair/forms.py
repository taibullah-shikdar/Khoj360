from django import forms

from .models import RepairRequest


class RepairRequestForm(forms.ModelForm):
    class Meta:
        model = RepairRequest
        fields = ("repair_type", "description", "budget", "phone", "location")
