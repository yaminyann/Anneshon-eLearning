# Generated by Django 4.2.5 on 2024-08-12 15:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Courses', '0015_courses_upload_certificate_courses_upload_deadline'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paid', models.BooleanField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='CourseItem', to='Courses.courses_upload')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='UserCourse', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
