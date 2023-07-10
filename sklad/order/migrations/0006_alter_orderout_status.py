# Generated by Django 4.2.3 on 2023-07-08 00:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_orderout_status_alter_orderout_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderout',
            name='status',
            field=models.CharField(choices=[('option1', 'Подготовка к отправке'), ('option2', 'В пути'), ('option3', 'Прибыл в пункт назначения')], max_length=50),
        ),
    ]
