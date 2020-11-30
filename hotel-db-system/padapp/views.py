from django.shortcuts import render, redirect, get_object_or_404
from .models import RoomServiceType, RoomService
# Item, OrderItem, Order
from UserApp.models import Guest

# Create your views here.
def pad_item_list(request):
    return render(request, 'pad.html')

def room_service(request):
    menu_pns = RoomServiceType.objects.filter(menu_type="PNS")
    menu_grill = RoomServiceType.objects.filter(menu_type="GRILL")
    menu_des = RoomServiceType.objects.filter(menu_type="DES")
     # for test
    return render(request, 'roomservice.html', {'pns':menu_pns, 'grill':menu_grill, 'des':menu_des})

def add_cart(request, item_id):
    pad_id = 2
    item = RoomServiceType.objects.get(pk=item_id)
    test= RoomService.objects.filter(selected_menu=item)

    try:
        cart = RoomService.objects.get(pad_id=2, selected_menu=item)
        if cart:
            if cart.selected_menu.menu_name == item.menu_name:
                cart.count +=1
                cart.save()
    except RoomService.DoesNotExist:
        # new_item = RoomService.objects.create(pad_id=pad_id, is_roomservice=True, selected_menu=item, count=1)
        cart = RoomService(
            pad_id=2,
            is_roomservice=True,
            selected_menu = item,
            count=1,
        )
        cart.save()
    
    # items = RoomService.objects.all()
    return redirect('padapp:cart')


def cart(request):
    cart_items = RoomService.objects.filter(pad_id=2)
    total_price = 0
    for each_total in cart_items:
        total_price += each_total.selected_menu.price * each_total.count
    if cart_items is not None:
        context={
            'cart_items':cart_items,
            'total_price':total_price,
        }
        return render(request, 'rs_cart.html', context)
    return redirect('padapp:cart')
    # return render(request, 'rs_cart.html', {'cart_items':cart_items})


def finish_order(request):
    return redirect('padapp:pad')