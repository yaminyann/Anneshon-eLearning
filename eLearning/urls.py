from django.contrib import admin
from django.urls import path,include
from django.conf.urls import handler404
from pages.views import custom_page_not_found_view


handler404 = custom_page_not_found_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Courses.urls')),
    path('', include('Accounts.urls')),
    path('', include('pages.urls'))
]
