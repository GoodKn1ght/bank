# Generated by Django 5.1.3 on 2024-12-05 07:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_analitics_operation_olap"),
    ]

    operations = [
        migrations.CreateModel(
            name="Operation",
            fields=[
                ("ID", models.AutoField(primary_key=True, serialize=False)),
                (
                    "Money_Used",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=20),
                ),
                ("Time_Completed", models.DateTimeField()),
                ("Proccessing_Stage", models.CharField(max_length=255)),
                ("Operation_Type", models.CharField(max_length=255)),
                ("Time_started", models.DateTimeField()),
                (
                    "User_ID",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="users.user"
                    ),
                ),
            ],
        ),
    ]