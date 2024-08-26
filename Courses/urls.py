from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.HomePage, name='HomePage'),
    path('404/', views.Page_Not_Found, name='404'),
    path('courses/category/<slug:category_slug>', views.Courses, name='Courses'),
    path('courses-details/<slug:slug>', views.CoursesDetails, name='courseDetails'),
    path('checkout/<slug:slug>', views.CheckOut, name='checkout'),
    path('my-courses/', views.My_Courses, name='myCourses'),
    path('courses/watch/<slug:slug>', views.Watch_Course, name='watch'),
    
    
    path('teacher-sales/', views.teacher_sales_view, name='teacher_sales'),
    
    
]+ static(settings.MEDIA_URL, document_root =settings.MEDIA_ROOT)