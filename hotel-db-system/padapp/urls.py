from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

app_name = "padapp"
urlpatterns = [
    path('', views.pad_item_list, name="pad"),
    path('roomservice/',views.room_service, name="roomservice"),
    path('roomservice/add_cart/<int:item_id>', views.add_cart, name="add_cart"),
    path('roomservice/cart/', views.cart, name="cart"),
    path('roomservice/order/', views.finish_order, name="order"),
    path('complain/', views.complain_list, name="complain"),
    path('complain/machine/', views.complain_machine, name="complain_machine"),

    # path('roomservice/ask/',views.add_cart_ask, name="ask"),
    # path('mycart/',views.my_cart, url_name="rs_ordered_list"),

    # path('roomservice/<int:menu_id>', views.rs_item_detail, name="item-detail"),
    # path('rs/order_check/<int:order_id>',views.rs_order_check, url_name="rs_order_check"),
    # path('dnd_td/', views.dnd_td, url_name="dnd_td"),
    # path('dnd/request/', views.dnd_request, url_name="dnd_request"),
    # path('td/request/',views.td_request, url_name="td_request"),
    # path('complain/write/', views.complain_list, url_name="complain_write"),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)