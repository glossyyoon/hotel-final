from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from .models import Guest
import json
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login

# Create your views here.


def guest_login(request):
    return render(request, 'UserApp/login.html')


def staff_login(request):
    return render(request, 'UserApp/staff_login.html')


def signup_submit(request):

    if request.method == 'POST':

        site_id = request.POST.get('id')
        site_pw = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        nation = request.POST.get('nation')
        birth = request.POST.get('birth')
        userGender = request.POST.get('userGender')
        last_name = request.POST.get('last_name')

        guest = Guest()
        guest.site_id = site_id
        guest.site_pw = site_pw
        guest.first_name = first_name
        guest.last_name = last_name

        guest.save()
        return render(request, 'UserApp/login.html')
    return render(request, 'UserApp/signup.html')


def login_submit(request):
    return render(request, 'UserApp/signup.html')


def signup(request):
    return render(request, 'UserApp/signup.html')


def logout(request):
    return render(request, 'UserApp/logout.html')


def guest_mypage(request):
    return render(request, 'UserApp/mypage.html')
