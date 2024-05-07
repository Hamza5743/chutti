import datetime

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction

from chutti.models import Leave, LeavesLeft, LeaveType, UserConstants


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

        if (
            leave_type_left == 0
            and getattr(LeaveType, self.cleaned_data["leave_type"])
            == LeaveType.MEDICAL_LEAVE
        ):
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


class AddLeavesForm(forms.Form):
    on_leave = forms.IntegerField(required=False)
    medical_leave = forms.IntegerField(required=False)
    casual_leave = forms.IntegerField(required=False)
    half_leave = forms.IntegerField(required=False)
    short_leave = forms.IntegerField(required=False)

    def clean(self):
        cleaned_data = super().clean()
        for _, value in cleaned_data.items():
            if value is not None and value < 0:
                raise ValidationError("Leaves count can't be negative")

    @transaction.atomic
    def save(self, user):
        leaves_left_for_year = LeavesLeft.get_current_object(user=user)
        if not leaves_left_for_year:
            leaves_left_for_year = LeavesLeft(user=user)

        for leave_type, value in self.cleaned_data.items():
            if value is not None:
                setattr(
                    leaves_left_for_year,
                    leave_type,
                    value,
                )

        user_constants = next(
            iter(UserConstants.objects.filter(user=user)),
            None,
        )

        if not user_constants:
            user_constants = UserConstants(user=user)

        user_constants.has_seen_add_leaves_page = True

        user_constants.save()
        leaves_left_for_year.save()
        return ""


class SignUpForm(UserCreationForm):
    def clean_username(self):
        self.clean()
        username: str = self.cleaned_data["username"]
        validate_email(username)
        return username


class LoginForm(AuthenticationForm):
    def clean_username(self):
        self.clean()
        username: str = self.cleaned_data["username"]
        validate_email(username)
        return username
