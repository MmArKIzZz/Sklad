# Generated by Django 4.2.3 on 2023-07-07 22:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderout',
            name='amount',
        ),
    ]
