from django.shortcuts import render, redirect
from .models import RoomServiceType, RoomService

# Create your views here.
def pad_item_list(request):
    return render(request, 'pad.html')

def room_service(request):
    menu_pns = RoomServiceType.objects.filter(menu_type="PNS")
    menu_grill = RoomServiceType.objects.filter(menu_type="GRILL")
    menu_des = RoomServiceType.objects.filter(menu_type="DES")
     # for test
    menu = RoomServiceType.objects.filter(menu_type="PNS")
    return render(request, 'roomservice.html', {'pns':menu_pns, 'grill':menu_grill, 'des':menu_des, 'menu':menu})

def rs_item_detail(request, menu_id):
    menu = RoomServiceType.objects.get(id=menu_id)
    menu_name = menu.menu_name
    return render(request, 'rs_menu_detail.html', {'menu_name':menu_name})