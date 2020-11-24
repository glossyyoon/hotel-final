from django.shortcuts import render, redirect
from .models import RoomServiceType, RoomService

# Create your views here.
# def pad_item_list(request):
#     return redirect('padapp:pad')

def room_service(request):
    menu = RoomServiceType.objects.all()

    return render(request, 'roomservice.html', {'menu':menu})