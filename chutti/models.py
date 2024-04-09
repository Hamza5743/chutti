from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models


class TotalLeaves(models.IntegerChoices):
    ON_LEAVE = 25
    MEDICAL_LEAVE = 10
    CASUAL_LEAVE = 20
    HALF_LEAVE = 15
    SHORT_LEAVE = 30


class LeaveType(models.TextChoices):
    ON_LEAVE = "On Leave"
    MEDICAL_LEAVE = "Medical Leave"
    CASUAL_LEAVE = "Casual Leave"
    HALF_LEAVE = "Half Leave"
    SHORT_LEAVE = "Short Leave"


class LeavesLeft(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    year = models.IntegerField(default=datetime.today().year)

    on_leave = models.IntegerField(default=TotalLeaves.ON_LEAVE)
    medical_leave = models.IntegerField(default=TotalLeaves.MEDICAL_LEAVE)
    casual_leave = models.IntegerField(default=TotalLeaves.CASUAL_LEAVE)
    half_leave = models.IntegerField(default=TotalLeaves.HALF_LEAVE)
    short_leave = models.IntegerField(default=TotalLeaves.SHORT_LEAVE)

    def convert_leave_name_to_attribute(self, leave_name):
        return f"{leave_name.replace(' ', '_').lower()}s"

    @classmethod
    def get_current_object(cls, user):
        return next(
            iter(LeavesLeft.objects.filter(year=datetime.today().year, user=user)),
            None,
        )


class Leave(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date_of_leave = models.DateField()
    leave_type = models.TextField(choices=LeaveType.choices, default=LeaveType.ON_LEAVE)
    description = models.TextField(default="")

    def __str__(self):
        return f"date_of_leave: {self.date_of_leave}, leave_type: {self.leave_type}, description: {self.description}"
