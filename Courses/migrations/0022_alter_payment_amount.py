# Generated by Django 4.2.5 on 2024-08-21 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Courses', '0021_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
