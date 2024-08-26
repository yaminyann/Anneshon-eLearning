from django.db.models.signals import post_save
from django.dispatch import receiver
from . models import UserCourse
from . views import update_sales

@receiver(post_save, sender=UserCourse)
def handle_course_purchase(sender, instance, created, **kwargs):
    if instance.paid:
        update_sales(instance.course)