from django.contrib import admin
from . models import *




@admin.register(Contact)
class Contact_Admin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message']
