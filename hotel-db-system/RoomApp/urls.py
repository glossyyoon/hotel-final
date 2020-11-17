from django.urls import path
from . import views
from .views import RoomListView, BookingListView, RoomDetailView, CancelBookingView

app_name = "RoomApp"

urlpatterns = [
    path('', views.main, name = "main"),
    path('available', RoomDetailView.as_view(), name = "RoomDetailView"),
    # path('room/<category>', RoomDetailView.as_view(), name='RoomDetailView'),
    path('list', RoomListView, name = "RoomListView"),
    path('booking/cancel/<pk>', CancelBookingView.as_view(), name='CancelBookingView'),
]
# urlpatterns = [
#     path('', RoomListView, name='RoomListView'),
#     path('booking_list/', BookingListView.as_view(), name='BookingListView'),
#     path('room/<category>', RoomDetailView.as_view(), name='RoomDetailView'),
#     path('booking/cancel/<pk>', CancelBookingView.as_view(),
#          name='CancelBookingView')

# ]