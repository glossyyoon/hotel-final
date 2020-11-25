from django.shortcuts import render, redirect
from .models import RoomServiceType, RoomService

# Create your views here.
def pad_item_list(request):
    return render(request, 'pad.html')

def room_service(request):
    menu_pns = RoomServiceType.objects.filter(menu_type="PNS")
    menu_grill = RoomServiceType.objects.filter(menu_type="GRILL")
    menu_des = RoomServiceType.objects.filter(menu_type="DES")
    
    return render(request, 'roomservice.html', {'pns':menu_pns, 'grill':menu_grill, 'des':menu_des})