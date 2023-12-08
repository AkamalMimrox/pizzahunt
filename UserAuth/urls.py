from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login_user,name='login'),
    path('register/',views.register_user,name='register'),
    path('userprofile/<int:id>/',views.user_profile,name='userprofile'),
    path('logout/',views.logout_user,name='logoutuser'),
    path('forgot-password/',views.forgot_password,name="forgot-password"),
    path('change-password/<token>/',views.changepassword,name='change-password'),
    path('error-404/',views.error_404,name='404')
]
