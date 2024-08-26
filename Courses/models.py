from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save


# Category models
class Course_Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    icon = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    
    
# Sub Category models 
class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(Course_Category, related_name='subcategories', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'category')
        
        
        
# Author - Teacher
class Author(models.Model): 
    author_profile = models.ImageField(upload_to="author")
    name = models.CharField(max_length=100, null=True)
    author_academic_or_skills_qualification = models.CharField(max_length=100, blank=True, null=True)
    about_author = models.TextField()

    def __str__(self):
        return self.name


# Course 
class Courses_Upload(models.Model):
    STATUS = (
        ('PUBLISH','PUBLISH'),
        ('DRAFT','DRAFT')
    )
    featured_image = models.ImageField(upload_to="featured_img", null=True)
    featured_video = models.CharField(max_length=300, null=True)
    title = models.CharField(max_length=500)
    created_at = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Course_Category, on_delete=models.CASCADE, related_name='Category_Wise_Course')
    description = models.TextField()
    price = models.IntegerField(null=True, default=0)
    discount = models.IntegerField(null=True)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)
    status = models.CharField(choices=STATUS, max_length=100, null=True)
    deadline = models.CharField(max_length=100,null=True)       
    certificate = models.BooleanField(default=False)
    # author_panel = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("courseDetails", kwargs={"slug": self.slug})
    
    
    
def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
        qs = Courses_Upload.objects.filter(slug=slug).order_by('-id')
        exists = qs.exists()
        if exists:
            new_slug = "%s-%s" % (slug, qs.first().id)
            return create_slug(instance, new_slug=new_slug)
        return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Courses_Upload)


# requirement and what you will learn models
class What_You_Learn(models.Model):
    course = models.ForeignKey(Courses_Upload, on_delete=models.CASCADE, related_name='learn_points')
    points = models.CharField(max_length=200)
    
    def __str__(self):
        return self.points
     
class Requirements(models.Model):
    course = models.ForeignKey(Courses_Upload, on_delete=models.CASCADE, related_name='requirement_points')
    points = models.CharField(max_length=500)
    
    def __str__(self):
        return self.points
    
    
# Lesson model
class Lesson(models.Model):
    course = models.ForeignKey(Courses_Upload, on_delete=models.CASCADE, related_name='lesson_points')
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name + " - " + self.course.title

class Video(models.Model):
    serial = models.IntegerField(null=False)
    course = models.ForeignKey(Courses_Upload, on_delete=models.CASCADE, related_name='video_points')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='points')
    title = models.CharField(max_length=300)
    youtube_id = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to="Thumbnail", null=True)
    time_duration = models.IntegerField(null=True)
    preview = models.BooleanField(default=False)
    
    
# user course 
class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='UserCourse')
    course = models.ForeignKey(Courses_Upload, on_delete=models.CASCADE, related_name='CourseItem')
    paid = models.BooleanField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.first_name + " - " + self.course.title
    

# paid course payment model  
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Payments')
    course = models.ForeignKey(Courses_Upload, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20)
    sender_mobile = models.CharField(max_length=15)
    transaction_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Payment by {self.user.username} for {self.course.title}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.verified:
            user_course, created = UserCourse.objects.get_or_create(user=self.user, course=self.course)
            if created:
                user_course.paid = True
                user_course.save()
    
# newsletter subscribe model
class Newsletter_Email(models.Model):
    email = models.EmailField(unique=True)
    time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email



    
# Course sales
class Course_Sales(models.Model):
    course = models.ForeignKey(Courses_Upload, on_delete=models.CASCADE, related_name="sales_course_name")
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teacher_sales')
    sales_count = models.IntegerField(default=0)
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    teacher_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    admin_earning = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.course.title} - {self.teacher.username} - {self.sales_count} sales"
    
