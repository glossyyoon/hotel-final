from django.urls import path
from . import views

app_name = "taskapp"
urlpatterns = [
    path('send/', views.request_send, name='request_send'),
    path('accept/', views.request_accept, name='request_accept'),
    path('reject/', views.request_reject, name='request_reject'),
    path('complete/', views.request_complete, name='request_complete'),
    path('cancel/', views.request_cancel, name='request_cancel'),
    path('assign/', views.request_assign, name='request_assign'),
    path('getList/', views.request_get_list, name='request_get_list'),
]