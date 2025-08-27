from datetime import date
from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["start_date", "end_date"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        today = date.today().isoformat()
        # HTML5 min-Attribute
        self.fields["start_date"].widget.attrs["min"] = today
        self.fields["end_date"].widget.attrs["min"] = today

    def clean(self):
        cleaned = super().clean()
        s = cleaned.get("start_date")
        e = cleaned.get("end_date")
        today = date.today()

        if s and s < today:
            self.add_error("start_date", "Startdatum darf nicht in der Vergangenheit liegen.")
        if e and e < today:
            self.add_error("end_date", "Enddatum darf nicht in der Vergangenheit liegen.")
        if s and e and e < s:
            raise forms.ValidationError("Enddatum darf nicht vor dem Startdatum liegen.")

        return cleaned
