from django.contrib import admin

from .models import Guest, Staff, Sales, Robot, Attendance, StaffLeave

admin.site.register(Guest)
admin.site.register(Staff)
admin.site.register(Sales)
admin.site.register(Robot)
admin.site.register(Attendance)
admin.site.register(StaffLeave)


# Register your models here.
