# Generated by Django 2.2.19 on 2021-06-08 08:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_auto_20210608_1154'),
    ]

    operations = [
        migrations.RenameField(
            model_name='form',
            old_name='form_id',
            new_name='id',
        ),
    ]