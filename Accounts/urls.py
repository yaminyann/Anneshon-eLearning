from django.urls import path
from . import views
from django.urls import include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('accounts/register', views.SignUp, name='signUP'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/',views.Login, name='Login'),
    path('accounts/profile', views.Profile, name='profile'),
    path('accounts/profile/update', views.Profile_Update, name='profile_Update'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]
