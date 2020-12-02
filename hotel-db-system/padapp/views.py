from django.shortcuts import render, redirect, get_object_or_404
from .models import RoomServiceType, RoomService, Complain
from TaskApp.views import request_send
from TaskApp.models import Request
from UserApp.models import Guest
from django.http import HttpRequest, QueryDict
import json

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
    
    for item in cart_items: #cart_items 에 담긴 roomservice_id 값 중 가장 큰 것으로 모두의 roomservice_num 값 설정하기        
        items_id=[]
        items_id.append(item.id)
    max_id = max(items_id)
    for each_rs_num in cart_items:
        each_rs_num.roomservice_num=max_id
        each_rs_num.save()

    if cart_items is not None:
        #template에 보낼 context
        context={
            'cart_items':cart_items,
            'total_price':total_price,
        }
        return render(request, 'rs_cart.html', context)
    return redirect('padapp:cart')
    # return render(request, 'rs_cart.html', {'cart_items':cart_items})


def finish_order(request):
    cart_items = RoomService.objects.filter(pad_id=2)
    # task로 data 보내기
    data = {
        'type': Request.RequestType.ROOM_SERVICE,
        'send_guest_id' : 2,
        'comment' : "RoomService Order",
        'roomservice_num': cart_items[0].roomservice_num
    }
    request = HttpRequest()
    request.method = 'POST'
    request.POST = data
    request_send(request)
    
    # # 주문 request를 보냈기 때문에 cart는 삭제한다.    --> 삭제하면 안돼 !!
    # for each_item in cart_items:
    #     each_item.delete()

    return redirect('padapp:pad')

def complain_list(request):
    pad_id = 2
    return render(request,'complain_list.html', {'pad_id':pad_id})

def complain_machine(request):
    return render(request, 'complain_machine.html')

def complain_machine_create(request, c_type):
    #   new_complain = Complain.objects.create(pad_id=pad_id, is_roomservice=True, selected_menu=item, count=1)

    if(request.method=='POST'):
        post = Complain()
        post.pad_id = 2
        post.is_complain=True
        post.complain_type=c_type
        post.content = request.POST['content']
        post.save()

        data={
            'type':Request.RequestType.ROOM_ETC,
            'send_guest_id':2,
            'comment': post.content
        }
        request=HttpRequest()
        request.method='POST'
        request.POST=data
        request_send(request)

    return redirect('padapp:pad')