# Generated by Django 4.2.9 on 2024-01-27 18:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="product", old_name="categroy", new_name="category",
        ),
    ]