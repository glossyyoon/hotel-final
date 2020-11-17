from django.urls import path
from . import views

app_name = "padapp"
urlpatterns = [
    path('pad/', views.pad_item_list, url_name="pad"),
    path('roomservice/',views.room_service, url_name="roomservice"),
    path('rs_order_check/<int:order_id>',views.rs_order_check, url_name="rs_order_check"),
    path('rs_ordered_list/',views.rs_ordered_list, url_name="rs_ordered_list"),
    
]
