from django.contrib import admin
from .models import Pad,RoomServiceType, RoomService, Dnd, TurnDown, Complain


class ComplainAdmin(admin.ModelAdmin):
    list_display=('id','complain_type','pad_id')

class RoomServiceAdmin(admin.ModelAdmin):
    list_display=('id', 'roomservice_num', 'pad_id', 'selected_menu', 'created_date')

# Register your models here.
admin.site.register(Pad)
admin.site.register(RoomServiceType)
# admin.site.register(OrderItem)
admin.site.register(RoomService, RoomServiceAdmin)
admin.site.register(Dnd)
admin.site.register(TurnDown)
admin.site.register(Complain, ComplainAdmin)


