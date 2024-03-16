import datetime

from django import forms
from django.core.exceptions import ValidationError

from .models import LeaveType


class LeaveForm(forms.Form):
    date_of_leave = forms.DateField()
    leave_type = forms.ChoiceField(choices=zip(LeaveType.names, LeaveType.values))
    description = forms.CharField(max_length=100, required=False)

    def clean_date_of_leave(self):
        data = self.cleaned_data["date_of_leave"]

        today = datetime.date.today()

        if data < today - datetime.timedelta(
            weeks=4
        ) or data > today + datetime.timedelta(weeks=4):
            raise ValidationError("You can only select date within 4 weeks of today")

        return data
