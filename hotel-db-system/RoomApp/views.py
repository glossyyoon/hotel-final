from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.generic import ListView, FormView, View, DeleteView
from django.urls import reverse, reverse_lazy
from .models import Room, Booking, Bill
from .forms import AvailabilityForm
from RoomApp.booking_functions.available import check_availability

import os
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
# Create your views here.
def main(request):
    return render(request, 'reserve_main.html', {})

def reserve_complete(request):
    return render(request, 'reserve_complete.html', {})

    
def RoomListView(request):
    rooms = Room.objects.all()[:]
    bookings = Booking.objects.all()[:]
    check_in = int(request.POST['check_in'].replace('-',''))
    check_out = int(request.POST['check_out'].replace('-',''))
    room_categories = dict(Room.room_type)
    room_list = []
    for room_category in room_categories:
        room = room_categories.get(room_category)
        room_url = reverse('roomapp:Reserve', kwargs={
                           'category': room_category,
                           })

        room_list.append((room, room_url))
    context = {
        "room_list": room_list,
        'check_in':check_in,
        'check_out':check_out
    }
    # room_list = [i.room_id for i in rooms]
    # for booking in bookings:
    #     chk_in = str(booking.check_in_date)[0:10].replace('-', '')
    #     chk_out = str(booking.check_out_date)[0:10].replace('-', '')
    #     if int(chk_in)>=check_in and check_out<=int(chk_out):
    #         roomnum = str(booking.booking_roomid)
    #         room_list.remove(int(roomnum[:3]))
    # reserve_room_num = request.POST.get('reserve_room_num', '')
    
    return render(request, 'reserve_list.html', {'check_in':check_in, 'check_out':check_out, 'room_list':room_list, 'bookings':bookings, 'context':context })


def Reserve(request, category):
    if request.method=="POST":
        booking = Booking.objects.create(
            booking_roomid = 201,
            check_in_date = request.POST.get('check_in',''),
            check_out_date = request.POST.get('check_out'),
            # user=self.request.user,
        )
        
        bill = Bill.objects.create(
            bill_room = booking.room_id,
            card_cvc_num = request.POST['cvc'],
            card_experiment = request.POST['card_experiment'],
            card_password = request.POST['card_password'],
        )

        reserve_room_num = request.POST.get('reserve_room' ''),
        cvc = request.GET.get('card_cvc_num')
        booking.save()
        bill.save()
    return render(request, 'reserve.html')


            
class BookingListView(ListView):
    model = Booking
    template_name = "booking_list_view.html"

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.all()
            return booking_list
        else:
            booking_list = Booking.objects.filter(user=self.request.user)
            return booking_list

class CancelBookingView(DeleteView):
    model = Booking
    template_name = 'booking_cancel_view.html'
    success_url = reverse_lazy('hotel:BookingListView')