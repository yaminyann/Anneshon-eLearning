from django.contrib import admin
from . models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Courses app register

# Category
@admin.register(Course_Category)
class Category_Admin(admin.ModelAdmin):
    list_display = ['id','name','icon','description','created_at','updated_at']
    
# Sub-Category
@admin.register(SubCategory)
class SubCategory_Admin(admin.ModelAdmin):
    list_display = ['id','name','icon','description','category','created_at','updated_at']
    
# Author
@admin.register(Author)
class Author_Admin(admin.ModelAdmin):
    list_display = ['id','author_profile','name','author_academic_or_skills_qualification','about_author']

# newsletter 
@admin.register(Newsletter_Email)
class Newsletter_Email_Admin(admin.ModelAdmin):
    list_display = ['email','time'] 
# Course
# @admin.register(Courses_Upload)
# class SubCategory_Admin(admin.ModelAdmin):
#     list_display = ['id','featured_image','featured_video','title','created_at','author','category','description','price','discount','status']
    


class What_You_Learn_TabularInLine(admin.TabularInline):
    model = What_You_Learn


    
class Requirements_TabularInLine(admin.TabularInline):
    model = Requirements



class Lesson_TabularInLine(admin.TabularInline):
    model = Lesson
    extra = 1
    def get_formset(self, request, obj=None, **kwargs ):
        formset = super().get_formset(request,obj,**kwargs)
        if obj:
            formset.form.base_fields['course'].queryset = Lesson.objects.filter(course=obj)
        return formset


    
class Video_TabularInLine(admin.TabularInline):
    model = Video


class Courses_Upload_Admin(admin.ModelAdmin):
    inlines = (What_You_Learn_TabularInLine,Requirements_TabularInLine,Lesson_TabularInLine,Video_TabularInLine)
    
    def get_form(self,request,obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        return form

# user course item
class UserCourseAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'paid', 'date']
    actions = ['mark_as_paid']

    def mark_as_paid(self, request, queryset):
        for UserCourse in queryset:
            UserCourse.paid = True
            UserCourse.save()

    mark_as_paid.short_description = "Mark selected courses as paid"
    
    
# paid course payment approve  
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user','verified','payment_method','amount','payment_date','course')
    list_filter = ['verified']
    search_fields = ('user__username', 'course__title')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.verified:
            obj.save()

admin.site.register(Payment, PaymentAdmin)

admin.site.register(UserCourse, UserCourseAdmin)
admin.site.register(Courses_Upload,Courses_Upload_Admin)
admin.site.register(Lesson)
admin.site.register(Course_Sales)




