from django.urls import path
from . import views


app_name = "userapp"
urlpatterns = [
    path('login/', views.guest_login, name='guest_login'),
    path('staff_login/', views.staff_login, name='staff_login'),
    path('signup/', views.signup, name='guest_signup'),
    path('signup_submit/', views.signup_submit, name='signup_submit'),
    path('login_post/', views.login_post, name='login_post'),
    path('logout/', views.logout, name='logout'),
    path('mypage/', views.guest_mypage, name='guest_mypage'),
    path('staff_attendance/', views.staff_attendance, name='staff_attendance'),
    path('staff_login_post/', views.staff_login_post, name='staff_login_post'),
    path('leave_request/', views.leave_request, name='leave_request'),
    path('attendance_request/', views.attendance_request, name='attendance_request')
]
