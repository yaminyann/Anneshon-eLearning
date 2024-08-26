from . import views
from django.urls import path


urlpatterns = [
    path('contact/', views.Contact_View, name='Contact'),
    path('terms-and-services/', views.TermsAndServices, name='termsNservices'),
    path('faq/', views.FAQ, name='faQ'),

]