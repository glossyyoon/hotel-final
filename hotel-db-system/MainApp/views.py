from django.shortcuts import render, redirect
from django.views.generic import ListView, FormView, View, DeleteView
from RoomApp.models import Booking

# Create your views here.


def main(request):
    check = 0
    user_id = ""
    if request.session.get('user'):
        user_id = request.session.get('user')
        check = 1
    return render(request, 'main.html', {'user_id': user_id, 'check': check})
