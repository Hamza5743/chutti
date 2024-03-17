from datetime import datetime

from django.contrib.auth import get_user_model
from django.db import models


class LeaveHours(models.IntegerChoices):
    FULL_LEAVE = 8
    PARTIAL_LEAVE = 4


class TotalLeaves(models.IntegerChoices):
    FULL_LEAVE = 4
    PARTIAL_LEAVE = 2


class LeaveType(models.TextChoices):
    FULL_LEAVE = "Full Leave"
    PARTIAL_LEAVE = "Partial Leave"


class LeavesLeft(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    year = models.IntegerField(default=datetime.today().year)

    full_leaves = models.IntegerField(default=TotalLeaves.FULL_LEAVE)
    partial_leaves = models.IntegerField(default=TotalLeaves.PARTIAL_LEAVE)

    def convert_leave_name_to_attribute(self, leave_name):
        return f"{leave_name.replace(' ', '_').lower()}s"

    def __str__(self):
        return f"year: {self.year}, full_leaves: {self.full_leaves}, partial_leaves: {self.partial_leaves}"


class Leave(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date_of_leave = models.DateField()
    leave_type = models.TextField(
        choices=LeaveType.choices, default=LeaveHours.FULL_LEAVE
    )
    description = models.TextField(default="")

    def __str__(self):
        return f"date_of_leave: {self.date_of_leave}, leave_type: {self.leave_type}, description: {self.description}"
