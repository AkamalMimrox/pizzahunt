from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login_user,name='login'),
    path('register/',views.register_user,name='register'),
    path('userprofile/<int:id>/',views.user_profile,name='userprofile'),
    path('logout/',views.logout_user,name='logoutuser')
]
