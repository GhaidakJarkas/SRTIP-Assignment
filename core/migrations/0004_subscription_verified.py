# Generated by Django 5.0.6 on 2024-05-16 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_subscription_passport_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]