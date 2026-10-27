from django import forms

from .models import MedicalReport, MedicalRequest


class MedicalRequestForm(forms.ModelForm):
    class Meta:
        model = MedicalRequest
        fields = (
            "request_type",
            "description",
            "phone",
            "location",
            "hospital",
            "blood_group",
            "blood_bags",
            "needed_at",
        )
        widgets = {
            "needed_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make blood_bags not required — default to 0 if left empty
        self.fields["blood_bags"].required = False
        self.fields["blood_bags"].initial = 0
        # Make other non-critical fields optional
        self.fields["description"].required = False
        self.fields["phone"].required = False
        self.fields["hospital"].required = False
        self.fields["blood_group"].required = False
        self.fields["needed_at"].required = False

    def clean_blood_bags(self):
        """If blood_bags left empty, return 0 instead of failing."""
        value = self.cleaned_data.get("blood_bags")
        if value is None or value == "":
            return 0
        return value


class MedicalReportForm(forms.ModelForm):
    class Meta:
        model = MedicalReport
        fields = ("reason",)
