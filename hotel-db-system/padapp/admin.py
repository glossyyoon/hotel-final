from django.contrib import admin
from .models import Pad, RoomService, Dnd, TurnDown, Complain
# Register your models here.
admin.site.register(Pad)
admin.site.register(RoomService)
admin.site.register(Dnd)
admin.site.register(TurnDown)
admin.site.register(Complain)



