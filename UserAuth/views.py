from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import UserAuthMaster
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


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
    
  