from django.urls import path
from . import views
from .views import (
    RoomListView,
    BookingListView,
    CancelBookingView,
    Reserve,
    reserve_complete,
)

app_name = "roomapp"

urlpatterns = [
    path("", views.main, name="main"),
    path("roomList", RoomListView, name="RoomListView"),
    path("reserve/<str:category>", views.Reserve, name="Reserve"),
    path("reserve_complete/", views.reserve_complete, name="reserve_complete"),
    path("booking/cancel/<pk>", CancelBookingView.as_view(), name="CancelBookingView"),
    path("get_booking_info", views.getBookingInfo, name="get_booking_info"),
    path("check_in", views.checkIn, name="check_in"),
    path("reserve/<str:category>", views.Reserve, name="Reserve"),
    path(
        "live_reservation_status",
        views.liveReservationStatusView,
        name="live_reservation_status",
    ),
]
# path('reserve/<int:reserve_room>', Reserve, name="Reserve"),
# urlpatterns = [
#     path('', RoomListView, name='RoomListView'),
#     path('booking_list/', BookingListView.as_view(), name='BookingListView'),
#     path('room/<category>', RoomDetailView.as_view(), name='RoomDetailView'),
#     path('booking/cancel/<pk>', CancelBookingView.as_view(),
#          name='CancelBookingView')

# ]