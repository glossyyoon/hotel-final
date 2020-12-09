from django.db import models
from django.conf import settings
from django.urls import reverse_lazy

# from PadApp.models import Pad

# Create your models here.


class Room(models.Model):
    room_id = models.IntegerField()
    room_type = (
        ("STD", "STANDARD"),
        ("SUP", "SUPERIOR"),
        ("DEL", "DELUXE"),
        ("EXC", "EXECUTIVE"),
        ("STE", "SUITE"),
    )
    room_limit = models.IntegerField()
    room_fee = models.IntegerField()
    on_use = models.BooleanField()
    # screen_id = models.ForeignKey("PadApp.Pad", on_delete=models.CASCADE)

    category = models.CharField(
        max_length=10, choices=room_type
    )  # 참고한 프로젝트에 있어서 일단 추가함.
    beds = models.IntegerField()  # 참고한 프로젝트에 있어서 일단 추가함.

    def __str__(self):
        return f"{self.room_id}. {dict(self.room_type)[self.category]} Beds = {self.beds} People = {self.room_limit}"


class Booking(models.Model):
    booking_roomid = models.ForeignKey(Room, null=True, on_delete=models.SET_NULL)
    booking_userid = models.ForeignKey(
        "UserApp.Guest", null=True, on_delete=models.SET_NULL
    )
    check_in = models.DateField(auto_now=False)
    check_out = models.DateField(auto_now=False)
    check_in_time = models.DateTimeField(auto_now=True, null=True)
    check_out_time = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"booking_room_id = {self.booking_roomid} check_in = {self.check_in} check_out = {self.check_out}"
        # return f'From = {self.check_in.strftime("%d-%b-%Y %H:%M")} To = {self.check_out.strftime("%d-%b-%Y %H:%M")}'

    def get_room_category(self):
        room_categories = dict(self.room.room_type)
        room_category = room_categories.get(self.room.category)
        return room_category

    def get_cancel_booking_url(self):
        return reverse_lazy(
            "hotel:CancelBookingView",
            args=[
                self.pk,
            ],
        )


class Bill(models.Model):
    bill_room = models.ForeignKey(Room, on_delete=models.CASCADE)
    card_cvc_num = models.PositiveIntegerField()
    card_experiment = models.PositiveIntegerField()
    card_password = models.PositiveIntegerField()
