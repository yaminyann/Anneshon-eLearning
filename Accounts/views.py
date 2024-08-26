from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import get_user_model , authenticate, login
from django.contrib.auth.backends import ModelBackend


# Accounts app view



# user registration
def SignUp(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # check email data
        if User.objects.filter(email=email).exists():
            messages.warning(request, 'Email are already exists !')
            return redirect('signUP')
        
        # Check username data
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Username are already exists !')
            return redirect('signUP')
        
        # save data 
        user = User(
            username = username,
            email = email,
        )
        user.set_password(password)
        user.save()
        messages.success(request, 'Signup successfully please login your anneshon account ')
        return redirect('Login')
    
    return render(request, 'registration/signup.html')



# Email Backend
class EmailBackEnd(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
        except UserModel.DoesNotExist:
            return None
            
        else:
            if user.check_password(password):
                return user
        return None
    
    
    
# login function
def Login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # check login data
        user = EmailBackEnd.authenticate(request, username=email, password = password)
        if user != None :
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Email and Password are Invalid, Try agin !')
            return redirect('Login')
    return render(request, 'registration/login.html')





# User profile
def Profile(request):
    return render(request, 'registration/profile.html')

# User profile update 
def Profile_Update(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id
        
        # pass User 
        user = User.objects.get(id=user_id)
        print(user, user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email = email
        
        if password != None and password != "":
            user.set_password(password)
        user.save()
        messages.success(request, 'Profile Update Successfully !')
        return redirect('profile')