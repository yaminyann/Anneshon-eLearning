# Generated by Django 4.2.5 on 2024-08-25 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Courses', '0025_alter_courses_upload_certificate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='course',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_points', to='Courses.courses_upload'),
        ),
    ]
