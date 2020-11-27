from django.urls import path
from . import views

app_name = "padapp"
urlpatterns = [
    path('', views.pad_item_list, name="pad"),
    path('roomservice/',views.room_service, name="roomservice"),
    path('roomservice/<int:menu_id>', views.rs_item_detail, name="item-detail"),
    path('roomservice/cart/<int:cart_id>', views.cart, name="cart"),
    path('roomservice/add_cart/<int:menu_id>', views.add_cart, name="add_cart"),
    # path('rs/order_check/<int:order_id>',views.rs_order_check, url_name="rs_order_check"),
    # path('rs/ordered_list/<int:order_id>',views.rs_ordered_list, url_name="rs_ordered_list"),
    # path('dnd_td/', views.dnd_td, url_name="dnd_td"),
    # path('dnd/request/', views.dnd_request, url_name="dnd_request"),
    # path('td/request/',views.td_request, url_name="td_request"),
    # path('complain/list/', views.complain_list, url_name="complain_list"),
    # path('complain/write/', views.complain_list, url_name="complain_write"),
]