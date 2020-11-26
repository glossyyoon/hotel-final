from django.shortcuts import render, redirect
from django.views.generic import ListView, FormView, View, DeleteView
from RoomApp.models import Booking

# Create your views here.


def main(request):
    return render(request, 'main.html')
