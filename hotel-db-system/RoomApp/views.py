from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.generic import ListView, FormView, View, DeleteView
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from datetime import datetime
import json
from django.http import JsonResponse, HttpResponse
from django.forms.models import model_to_dict

from .models import Room, Booking, Bill
from .forms import AvailabilityForm
from RoomApp.booking_functions.available import check_availability
from django.views.decorators.csrf import csrf_exempt
from UserApp.models import Guest

import os

# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
# Create your views here.
def main(request):

    return render(request, "reserve_main.html", {})


def reserve_complete(request):
    booking_room_id = request.session.get("num")[:3]
    find_room_num = Room.objects.filter(room_id=booking_room_id)[0]
    Bill.objects.get_or_create(
        bill_room=find_room_num,
        card_cvc_num=request.POST.get("card_cvc_num", ""),
        card_experiment=request.POST.get("card_experiment", ""),
        card_password=request.POST.get("card_password", ""),
    )
    return render(request, "reserve_complete.html", {})


@csrf_exempt
def checkIn(request):
    json_data = json.loads(request.body)
    room = Room.objects.get(room_id=json_data["room_id"])
    room.on_use = True
    room.save()
    room = model_to_dict(room)
    return JsonResponse({"room": room}, status=201)


def getBookingInfo(request):
    json_data = json.loads(request.body)
    date = json_data["date"]
    room = Room.objects.get(room_id=json_data["room_id"])
    booking = Booking.objects.get(
        booking_roomid=room.id, check_in__lte=date, check_out__gte=date
    )
    user = Guest.objects.get(pk=booking.booking_userid_id)
    booking = model_to_dict(booking)
    user = model_to_dict(user)
    return JsonResponse({"booking": booking, "user": user}, status=201)


def liveReservationStatusView(request):
    rooms = Room.objects.all().values()
    date = request.POST.get("Date", timezone.now())
    if isinstance(date, str):
        date = datetime.strptime(date, "%Y-%m-%d")
        date = timezone.make_aware(date)
    for room in rooms:
        checked_in = Booking.objects.filter(
            booking_roomid=room["id"], check_in__lte=date, check_out__gte=date
        )
        room["checked_in"] = len(checked_in) != 0
        room["is_using"] = len(checked_in) != 0 and room["on_use"]
    return render(
        request,
        "live_reservation_status.html",
        {"selected_date": str(date), "rooms": rooms},
    )


def RoomListView(request):
    rooms = Room.objects.all()[:]
    bookings = Booking.objects.all()[:]

    check_in = (request.POST["check_in"],)
    check_out = (request.POST["check_out"],)
    request.session["check_in"] = check_in
    request.session["check_out"] = check_out

    check_in_date = int(request.POST["check_in"].replace("-", ""))
    check_out_date = int(request.POST["check_out"].replace("-", ""))
    room_categories = dict(Room.room_type)
    room_list = []
    for room_category in room_categories:
        room = room_categories.get(room_category)
        room_url = reverse(
            "roomapp:Reserve",
            kwargs={
                "category": room_category,
            },
        )

        room_list.append((room, room_url))
    context = {"room_list": room_list, "check_in": check_in, "check_out": check_out}

    return render(
        request,
        "reserve_list.html",
        {
            "check_in": check_in,
            "check_out": check_out,
            "room_list": room_list,
            "bookings": bookings,
            "context": context,
        },
    )


@csrf_exempt
def Reserve(request, category):
    reserve_room_category = request.POST.get("category")

    check_in = request.session.get("check_in")[0]
    check_out = request.session.get("check_out")[0]
    if (check_in[0] == check_in[-1]) and check_in.startswith(("'", '"')):
        check_in = check_in[1:-1]
    if (check_out[0] == check_out[-1]) and check_out.startswith(("'", '"')):
        check_out = check_out[1:-1]
    # print(check_in, check_out)

    booking_room = Room.objects.filter(category=category).values("room_id")
    index = 0
    for i in range(len(booking_room) - 1):
        if (
            Booking.objects.filter(check_in__range=[check_in, check_out]).exists()
            or Booking.objects.filter(check_out__range=[check_in, check_out]).exists()
        ):
            index += 1
        else:
            break
    booking_room_id = Room.objects.filter(category=category)[index]
    booking_room_num = str(booking_room_id)
    request.session["num"] = booking_room_num
    # print(booking_room_id)
    # booking_room_room = booking_room_id.values

    booking_user_id = request.session.get("user")
    Booking.objects.get_or_create(
        booking_roomid=booking_room_id,
        booking_userid=Guest.objects.get(site_id=booking_user_id),
        check_in=check_in,
        check_out=check_out,
    )
    print(booking_room_id)

    return render(request, "reserve.html")


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
    template_name = "booking_cancel_view.html"
    success_url = reverse_lazy("hotel:BookingListView")
