# Generated by Django 4.2.9 on 2024-02-10 13:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0003_review"),
        ("order", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(old_name="OrderItems", new_name="OrderItem",),
    ]