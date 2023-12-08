from tokenize import generate_tokens
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import UserAuthMaster
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
import uuid
from django.utils import timezone

#Authentication Views



def login_user(request):
    if request.user.is_authenticated:
        return redirect('index')
    else:
        type = 'login'
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            if not (username and password):
                messages.error(request, message='All fields are required!')
            else:
                user = UserAuthMaster.objects.filter(username=username).first()
                if user:
                    auth_password = check_password(password, user.password)
                    if auth_password:
                        auth_user = authenticate(request, username=username, password=password)
                        if auth_user:
                            login(request, auth_user)
                            return redirect('index')
                        else:
                            messages.error(request, message='User is not authenticated!')
                    else:
                        messages.error(request, message="Password doesn't match!")
                else:
                    messages.error(request, message="User doesn't exist!")

        context = {
            "type": type
        }
    return render(request, 'userauth.html', context)



def register_user(request):
    type = 'register'

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        if not (username and email and password and cpassword):
            messages.error(request, message='All fields are required!')
        elif password != cpassword:
            messages.error(request, message='Password and Confirm do not match!')
        else:
            user = UserAuthMaster.objects.filter(username=username).first()
            if user:
                messages.error(request, message='Username is already taken!')
            else:
                new_user = UserAuthMaster(
                    username=username,
                    password=make_password(password=password),
                    email=email,
                )
                new_user.save()
                login(request, user=new_user)
                return redirect('index')

    context = {
        "type": type
    }
    return render(request, 'userauth.html', context)

@login_required(login_url='login/')
def user_profile(request, id):
    user = get_object_or_404(UserAuthMaster, id=id)

    if request.method == "POST":
        # Get the updated information from the form
        username = request.POST.get('username')
        email = request.POST.get('email')
        phonenumber = request.POST.get('phonenumber')
        userimage = request.FILES.get('userimage')
        

        # Update the user information
        user.username = username
        user.email = email
        user.phonenumber = phonenumber
        user.profile_image=userimage
        user.save()

        # Redirect to the user profile page
        return redirect('userprofile', id=id)

    context = {
        'user': user
    }
    return render(request, 'profile/user_profile.html', context)

def logout_user(request):
    logout(request)
    return redirect('index')
    
    
def forgot_password(request):
    email = request.POST.get('email')
    if request.method == "POST":
        user_obj = UserAuthMaster.objects.filter(email=email).first()
        if user_obj:
            # Set token and expiration time
            token = str(uuid.uuid4())
            expiration_time = timezone.now() + timezone.timedelta(hours=1)  # Set expiration time (1 hour in this example)
            
            user_obj.forgot_token = token
            user_obj.forgot_token_expiration = expiration_time
            user_obj.save()
            
            subject = 'reset password'
            message = f'Hi {user_obj.username}, your forget password link expires in 1 hour. Click here: http://127.0.0.1:8000/change-password/{token}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail(subject, message, email_from, recipient_list)
            
            messages.success(request, message='Email has been sent!')
        else:
            messages.error(request, message='User not found!')

    return render(request, 'forgot-password/forgot-password.html')

def changepassword(request, token):
    user_obj = UserAuthMaster.objects.filter(forgot_token=token).first()
    
    if user_obj:
        current_time = timezone.now()
        if current_time > user_obj.forgot_token_expiration:
            messages.error(request, 'The token has expired. Please request a new password reset link.')
            return render(request, 'forgot-password/expired-token.html')
        
        if request.method == "POST":
            new_password = request.POST.get('password')
            cpassword = request.POST.get('cpassword')

            if new_password and cpassword:
                if new_password != cpassword:
                    messages.error(request, "Password and confirm password do not match!")
                else:
                   
                    user_obj.password = make_password(new_password)
                    user_obj.forgot_token = "-"
                    user_obj.save()
                    messages.success(request, 'Password has been updated. You can now log in using the new password!')
            else:
                messages.error(request, "All fields are required!")

        return render(request, 'change-password/change-password.html', {'user_id': user_obj.id})
    else:
        return redirect('404')


def error_404(request):
    return render(request,'404/404.html')
  