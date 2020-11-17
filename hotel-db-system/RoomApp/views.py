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


def RoomListView(request):
    room = Room.objects.all()[0]
    room_categories = dict(room.room_type)
    room_values = room_categories.values()
    room_list = []

    for room_category in room_categories:
        room = room_categories.get(room_category)
        room_url = reverse('RoomApp:RoomListView', kwargs={
                           'category': room_category})

        room_list.append((room, room_url))
    context = {
        "room_list": room_list,
    }
    return render(request, 'reserve_list.html', context)


class RoomDetailView(View):
    # def get(self, request, *args, **kwargs):
    #     category = self.kwargs.get('category', None)
    #     form = AvailabilityForm()
    #     room_list = Room.objects.filter(category=category)

    #     if len(room_list) > 0:
    #         room = room_list[0]
    #         room_category = dict(room.room_type).get(room.category, None)
    #         context = {
    #             'room_category': room_category,
    #             'form': form,
    #         }
    #         return render(request, 'reserve.html', context)
    #     else:
    #         return HttpResponse('Category does not exist')
    def get(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        form = AvailabilityForm()
        room_list = Room.objects.filter(category=category)
        cate = Room.category
        # if len(room_list) > 0:
        # room = room_list[0]
        # room_category = dict(room.room_type).get(room.category, None)
        # context = {
        #     'room_category': room_category,
        #     'form': form,
        # }
        return render(request, 'reserve.html', {'cate':cate})
        # else:
            # return HttpResponse('Category does not exist')

    def post(self, request, *args, **kwargs):
        category = self.kwargs.get('category', None)
        room_list = Room.objects.filter(category=category)
        form = AvailabilityForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

        available_rooms = []
        for room in room_list:
            if check_availability(room, data['check_in'], data['check_out']):
                available_rooms.append(room)

        if len(available_rooms) > 0:
            room = available_rooms[0]
            booking = Booking.objects.create(
                user=self.request.user,
                room=room,
                check_in=data['check_in'],
                check_out=data['check_out']
            )
            booking.save()
            # message = Mail(
            #     from_email='dhabaledarshan@gmail.com',
            #     to_emails='dhabalekalpana@gmail.com',
            #     subject='Sending from hotelina',
            #     html_content='<strong>Sending from hotelina</strong>')
            try:
                # sg = SendGridAPIClient(env.str('SG_KEY'))
                # response = sg.send(message)
                # print(response.status_code)
                # print(response.body)
                # print(response.headers)
                print('SENT!!!')
            except Exception as e:
                print(e)
            return HttpResponse(booking)
        else:
            return HttpResponse('All of this category of rooms are booked!! Try another one')

class BookingListView(ListView):
    model = Booking

    def get_queryset(self, *args, **kwargs):
        booking_list = Booking.objects.all()
        return render(request, 'RoomApp:preview')


class CancelBookingView(DeleteView):
    model = Booking
    template_name = 'booking_cancel_view.html'
    success_url = reverse_lazy('hotel:BookingListView')
