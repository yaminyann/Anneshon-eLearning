# Generated by Django 4.2.5 on 2024-08-11 04:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Courses', '0012_lesson_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson_points', to='Courses.courses_upload'),
        ),
        migrations.AlterField(
            model_name='video',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='video_points', to='Courses.courses_upload'),
        ),
    ]
