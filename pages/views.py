from django.shortcuts import render,redirect
from pages.models import *
from django.contrib import messages


# contact 
def Contact_View(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        contact_entry = Contact(name=name, email=email, message=message)
        contact_entry.save()
        messages.success(request, 'Apnr form ti submit hoyeche')
        return redirect('Contact')
    
    return render(request, 'pages/contact.html')

def TermsAndServices(request):
    return render(request, 'pages/termsNservices.html')


# FAQ page
def FAQ(request):
    return render(request, 'pages/faq.html')


# 404 page show when url are wrong 
def custom_page_not_found_view(request, exception):
    return render(request, '404.html', status=404)


