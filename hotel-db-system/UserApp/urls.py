from django.urls import path
from . import views


app_name = "userapp"
urlpatterns = [
    path('login/', views.guest_login, name='guest_login'),
    path('staff_login/', views.staff_login, name='staff_login'),
    path('signup/', views.signup, name='guest_signup'),
    path('signup_submit/', views.signup_submit, name='signup_submit'),
    path('login_submit/', views.login_submit, name='login_submit'),
    path('logout/', views.logout, name='logout'),
    path('mypage/', views.guest_mypage, name='guest_mypage')
]
