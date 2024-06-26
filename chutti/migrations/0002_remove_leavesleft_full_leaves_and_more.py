# Generated by Django 5.0.1 on 2024-04-09 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chutti", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="leavesleft",
            name="full_leaves",
        ),
        migrations.RemoveField(
            model_name="leavesleft",
            name="partial_leaves",
        ),
        migrations.AddField(
            model_name="leavesleft",
            name="casual_leave",
            field=models.IntegerField(default=20),
        ),
        migrations.AddField(
            model_name="leavesleft",
            name="half_leave",
            field=models.IntegerField(default=15),
        ),
        migrations.AddField(
            model_name="leavesleft",
            name="medical_leave",
            field=models.IntegerField(default=10),
        ),
        migrations.AddField(
            model_name="leavesleft",
            name="on_leave",
            field=models.IntegerField(default=25),
        ),
        migrations.AddField(
            model_name="leavesleft",
            name="short_leave",
            field=models.IntegerField(default=30),
        ),
        migrations.AlterField(
            model_name="leave",
            name="leave_type",
            field=models.TextField(
                choices=[
                    ("On Leave", "On Leave"),
                    ("Medical Leave", "Medical Leave"),
                    ("Casual Leave", "Casual Leave"),
                    ("Half Leave", "Half Leave"),
                    ("Short Leave", "Short Leave"),
                ],
                default="On Leave",
            ),
        ),
    ]
