# Generated by Django 5.0 on 2024-06-18 13:24

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("members", "0002_member_has_key_member_phone_number"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="member",
            name="number",
        ),
    ]