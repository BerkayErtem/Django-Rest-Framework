# Generated by Django 2.2.19 on 2021-06-08 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_user_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.CharField(auto_created=True, max_length=50, primary_key=True, serialize=False, unique=True)),
                ('destination', models.CharField(max_length=50)),
                ('date', models.DateField()),
            ],
            options={
                'db_table': 'forms',
            },
        ),
    ]
