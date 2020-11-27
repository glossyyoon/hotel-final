from django.shortcuts import render, HttpResponse, redirect
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

def available(request):
    return render(request, 'reserve.html', {})

def reserve_complete(request):
    return render(request, 'reserve_complete.html', {})

class RoomListView(View):
    
    def get(self, request):
        rooms = Room.objects.all()[:]
        bookings = Booking.objects.all()[:]
        check_in = int(request.GET.get('check_in').replace('-',''))
        check_out = int(request.GET.get('check_out').replace('-',''))

        room_list = [i.room_id for i in rooms]
        for booking in bookings:
            chk_in = str(booking.check_in_date)[0:10].replace('-', '')
            chk_out = str(booking.check_out_date)[0:10].replace('-', '')
            if int(chk_in)>=check_in and check_out<=int(chk_out):
                roomnum = str(booking.booking_roomid)
                room_list.remove(int(roomnum[:3]))
        
        return render(request, 'reserve_list.html', {'check_in':check_in, 'check_out':check_out, 'room_list':room_list, 'bookings':bookings})

class Reserve(View):
    def post(self, request, *args, **kwargs):
        # if request.method=="POST":
        #     booking = Booking.objects.create(
        #         booking_roomid = reserve_room,
        #         user=self.request.user,
        #         room=room,
        #     )
        #     booking.save()
            

        return render(request, 'reserve_complete.html')

    def get(self, request):
        reserve_room = request.GET.get('reserve_room')
        cvc = request.GET.get('card_cvc_num')
        return render(request, 'reserve_complete.html', {'reserve_room':reserve_room, 'cvc':cvc})

            
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