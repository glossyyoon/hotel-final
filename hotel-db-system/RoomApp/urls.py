from django.urls import path
from . import views
from .views import RoomListView, BookingListView, CancelBookingView, Reserve, reserve_complete

app_name = "roomapp"

urlpatterns = [
    path('', views.main, name = "main"),
    # path('room/<category>', RoomDetailView.as_view(), name='RoomDetailView'),
    path('reserve_list', RoomListView.as_view(), name = "RoomListView"),
    path('booking/cancel/<pk>', CancelBookingView.as_view(), name='CancelBookingView'),
    path('reserve/', Reserve.as_view(), name = 'Reserve'),
    path('reserve_complete/', reserve_complete, name = 'reserve_compltete')
]
# urlpatterns = [
#     path('', RoomListView, name='RoomListView'),
#     path('booking_list/', BookingListView.as_view(), name='BookingListView'),
#     path('room/<category>', RoomDetailView.as_view(), name='RoomDetailView'),
#     path('booking/cancel/<pk>', CancelBookingView.as_view(),
#          name='CancelBookingView')

# ]