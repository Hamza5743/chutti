import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Leave, LeavesLeft, LeaveType


class LeaveForm(forms.Form):
    date_of_leave = forms.DateField()
    leave_type = forms.ChoiceField(choices=zip(LeaveType.names, LeaveType.values))
    description = forms.CharField(max_length=100, required=False)

    def clean_date_of_leave(self):
        data: datetime.date = self.cleaned_data["date_of_leave"]

        if not data.year == datetime.date.today().year:
            raise ValidationError("You can only select date of this year")

        return data

    @transaction.atomic
    def save(self, user):
        leaves_left_for_year = LeavesLeft.get_current_object(user=user)
        if not leaves_left_for_year:
            leaves_left_for_year = LeavesLeft(user=user)

        leave_type_left = getattr(
            leaves_left_for_year,
            leaves_left_for_year.convert_leave_name_to_attribute(
                self.cleaned_data["leave_type"]
            ),
        )

        if leave_type_left == 0:
            return f"You don't have any {getattr(LeaveType, self.cleaned_data['leave_type']).lower()}s left for the year"

        setattr(
            leaves_left_for_year,
            leaves_left_for_year.convert_leave_name_to_attribute(
                self.cleaned_data["leave_type"]
            ),
            leave_type_left - 1,
        )

        leave_request = Leave(
            user=user,
            date_of_leave=self.cleaned_data["date_of_leave"],
            leave_type=getattr(LeaveType, self.cleaned_data["leave_type"]),
            description=self.cleaned_data["description"],
        )

        leaves_left_for_year.save()
        leave_request.save()
        return ""
