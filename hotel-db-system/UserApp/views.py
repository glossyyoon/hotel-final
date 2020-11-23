from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import auth
from .models import Guest, Staff, Attendance
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


def staff_login_post(request):
    response_data = {}

    if request.method == "GET":
        return render(request, '/UserApp/staff_login.html')

    elif request.method == "POST":
        staff_id = request.POST.get('staff_id', None)

        staff = Staff.objects.filter(staff_id=staff_id).values()
        print(staff)
        if len(staff) == 0:
            response_data['error'] = "ID가 존재하지 않습니다."
        else:
            request.session['staff'] = staff[0]['id']
            return redirect('/userApp/staff_attendance/')

    return redirect('/userApp/staff_login')


def signup_submit(request):

    if request.method == 'POST':

        site_id = request.POST.get('id')
        site_pw = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        nation = request.POST.get('nation')
        birth = request.POST.get('birth')
        userGender = request.POST.get('userGender')
        email = request.POST.get('userEmail')

        guest = Guest()
        guest.site_id = site_id
        guest.site_pw = site_pw
        guest.first_name = first_name
        guest.last_name = last_name
        guest.nation = nation
        guest.birthday = birth
        guest.gender = userGender
        guest.email = email

        guest.save()
        return render(request, 'UserApp/login.html')
    return render(request, 'UserApp/signup.html')


def login_post(request):
    response_data = {}

    if request.method == "GET":
        return render(request, '/UserApp/login.html')

    elif request.method == "POST":
        login_id = request.POST.get('userId', None)
        login_password = request.POST.get('userPw', None)
        print(login_id)
        guest = Guest.objects.filter(site_id=login_id).values()
        if len(guest) == 0:
            response_data['error'] = "ID가 존재하지 않습니다."
        else:
            # db에서 꺼내는 명령. Post로 받아온 username으로 , db의 username을 꺼내온다.
            if login_password == guest[0]['site_pw']:
                request.session['user'] = guest[0]['site_id']
                # 세션도 딕셔너리 변수 사용과 똑같이 사용하면 된다.
                # 세션 user라는 key에 방금 로그인한 id를 저장한것.
                return redirect('/userApp/mypage/')
            else:
                response_data['error'] = "비밀번호를 틀렸습니다."

    return render(request, 'UserApp/login.html')


def signup(request):
    return render(request, 'UserApp/signup.html')


def logout(request):
    return render(request, 'UserApp/logout.html')


def guest_mypage(request):
    user_id = request.session.get('user')
    print(user_id)
    return render(request, 'UserApp/mypage.html', {'user_id': user_id})


def staff_attendance(request):
    staff_id = request.session.get('staff')
    staff = Staff.objects.filter(
        id=staff_id).values()
    attendance_list = Attendance.objects.filter(
        staff_id=staff_id).values()
    print(staff_attendance)
    print(staff)
    return render(request, 'UserApp/staff_attendance.html', {'staff_id': staff[0]['staff_id'], 'attendance_list': attendance_list})
