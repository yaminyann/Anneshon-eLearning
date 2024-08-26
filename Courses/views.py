from django.shortcuts import render,redirect,get_object_or_404
from . models import *
from .forms import *
from django.db.models import Sum,Count
from django.urls import reverse
from django.contrib import messages
from django.http import Http404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.validators import validate_email



# courses app views 
def HomePage(request):
    categories = Course_Category.objects.all().order_by('id')[0:5]
    course = Courses_Upload.objects.filter(status = 'PUBLISH').order_by('id')
    
    # popular courses
    popular_courses = Courses_Upload.objects.annotate(
        total_enrollments=Count('CourseItem')
    ).filter(total_enrollments__gt=0).order_by('-total_enrollments')[:5]
    
    # newsletter submission views
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            validate_email(email)
        except ValidationError :
            messages.error(request, 'enter valid email')
            return redirect(request.path)
        
        if Newsletter_Email.objects.filter(email=email).exists():
            messages.error(request, 'This email are already subscribe')
            return redirect(request.path)
        
        Newsletter_Email.objects.create(email=email)
        messages.success(request, 'Thanks for subscribing our newsletter !')
        return redirect(request.path)  
    
    
    context = {
        'category':categories,
        'course': course,
        'popular_courses':popular_courses,
    }
    return render(request, 'Courses/home.html',context)


# error page
def Page_Not_Found(request):
    return render(request, 'error/error.html')


# Course page
def Courses(request,category_slug):
    category = get_object_or_404(Course_Category, slug=category_slug)
    courses = Courses_Upload.objects.filter(category=category, status='PUBLISH')
    
    if courses.exists():
        # paginator 
        pagination = Paginator(courses, 9)
        page_number = request.GET.get('page')
        page = pagination.get_page(page_number)
        context = {
            'category':category,
            'page_object':page,
            
        }
        return render(request, 'Courses/courses.html',context)
    
    else:
        return redirect('404')



    



# course details
def CoursesDetails(request, slug):
    courses = get_object_or_404(Courses_Upload, slug=slug)
    related_course = Courses_Upload.objects.filter(category=courses.category).exclude(id=courses.id)[0:3]
    time_duration_minute = Video.objects.filter(course__slug = slug).aggregate(Sum('time_duration'))['time_duration__sum']
    shareable_link = request.build_absolute_uri(reverse('courseDetails', args=[slug]))
    
    # free course enroll
    course_id = Courses_Upload.objects.get(slug=slug)
    check_enroll = None
    if request.user.is_authenticated:
        try:
            check_enroll = UserCourse.objects.get(user = request.user, course = course_id)
        except UserCourse.DoesNotExist:
            check_enroll = None
    
    # count course time
    if time_duration_minute:
        hour = time_duration_minute // 60
        minute = time_duration_minute % 60
        
    else :
        minute = 0
        hour = 0
    
    # show error page when i hit wrong slug
    # when debug is False and Server host then it works
    # try:
    #     course = Courses_Upload.objects.get(slug=slug)
    # except Courses_Upload.DoesNotExist:
    #     redirect('404')
    
    # collect data from payment page
    if request.method == "POST":
        payment_method = request.POST.get('payment_method')
        sender_mobile = request.POST.get('sender_mobile')
        transaction_id = request.POST.get('transaction_id')
        amount = request.POST.get('amount')
        
        # check transaction id unique or not
        if Payment.objects.filter(transaction_id=transaction_id).exists():
            messages.error(request, 'tx id already used')
            return redirect('courseDetails',slug=courses.slug)
        
        # create payment object and show in admin panel
        Payment.objects.create(
            user=request.user,
            course=courses,
            payment_method=payment_method,
            sender_mobile=sender_mobile,
            transaction_id=transaction_id,
            amount = amount
        )
        return redirect('404')
    
    context = {
        'courses':courses,
        'total_duration_minute':minute,
        'total_duration_hours':hour,
        'shareable_link':shareable_link,
        'check_enroll':check_enroll,
        'related_course':related_course
    }

    return render(request, 'Courses/courseDetails.html',context)




# Checkout 
@login_required(login_url='/login/')
def CheckOut(request, slug):
    course = Courses_Upload.objects.get(slug=slug)
    if course.price == 0 :
        course = UserCourse(
            user = request.user,
            course = course
        )
        course.save()
        messages.success(request, 'Congratulations - Apni Course a successfully enrolled korechen !')
        return redirect('myCourses')


    
    
# My Courses
def My_Courses(request):
    course = UserCourse.objects.filter(user=request.user)
    context = {
        'course':course,
    }
    return render(request, 'Courses/my_course.html', context)
    






# Watch course Video
def Watch_Course(request,slug):
    course = Courses_Upload.objects.filter(slug=slug)

    if course.exists():
        course = course.first()
    else:
        return redirect('404')
    context = {
        'course':course,
    }
    return render(request, 'Courses/watch.html', context)


















# sales Count
def update_sales(course):
    sales_amount = course.price - (course.price * (course.discount or 0) / 100)  #
    

    course_sales, created = Course_Sales.objects.get_or_create(course=course, teacher=course) 

    course_sales.sales_count += 1
    course_sales.total_earnings += sales_amount
    course_sales.teacher_earnings += (sales_amount * 0.75) 
    course_sales.admin_earnings += (sales_amount * 0.25)  
    course_sales.save()

    
    

def teacher_sales_view(request):

    courses = Courses_Upload.objects.filter(author=request.user)  #

    context = {
        'courses': courses,
    }
    return render(request, 'teacher_sales.html', context)
