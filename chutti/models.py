from django.contrib.auth import get_user_model
from django.db import models


class LeaveHours(models.IntegerChoices):
    FULL_LEAVE = 8
    PARTIAL_LEAVE = 4


class TotalLeaves:
    FULL_LEAVE = 4
    PARTIAL_LEAVE = 2


class LeavesLeft(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    year = models.DateField()

    full_leaves = models.IntegerField(default=TotalLeaves.FULL_LEAVE)
    partial_leaves = models.IntegerField(default=TotalLeaves.PARTIAL_LEAVE)


class Leave(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    date_of_leave = models.DateField()
    leave_hours = models.IntegerField(
        choices=LeaveHours.choices, default=LeaveHours.FULL_LEAVE
    )
