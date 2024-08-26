from django.shortcuts import render,redirect,HttpResponseRedirect
from . models import *
from Accounts.models import *
from . views import *
from django.db.models import Sum


def Send_Context(request):
    categories = Course_Category.objects.all()
    context = {
        'categories':categories,
    }
    return context
    

    