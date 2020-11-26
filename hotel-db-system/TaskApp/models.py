from django.db import models
from django.utils.translation import gettext_lazy as _


class ProductRequest(models.Model):
    staff_id = models.ForeignKey(
        'UserApp.Staff', on_delete=models.CASCADE, null=True)
    product_item = models.CharField(max_length=100)
    product_count = models.IntegerField(default=1)
    product_from = models.DateTimeField(auto_now=True)
    product_to = models.DateTimeField(auto_now=False)


class Request(models.Model):

    class RequestType(models.TextChoices):
        ROOM_CLEANING = 'Room_Cleaning', _('Room_Cleaning')
        ROOM_SERVICE = 'Room_Service', _('Room_Service')
        ROOM_ERROR = 'Room_Error', _('Room_Error')
        ROOM_ETC = "Room_ETC", _('Room_ETC')
        CARRY_IN = "Carry_In", _('Carry_In')
        CARRY_OUT = "Carry_Out", _('Carry_Out')
        VALET_PARKING = "Valet_Parking", _('Valet_Parking')
        PRODUCT_PURCHASING = "Product_Purchasing", _('Product_Purchasing')
        CARRY_ROOM_SERVICE = "Carry_Room_Service", _('Carry_Room_Service')
        ETC = "ETC", ('ETC')

    class RequestStatus(models.TextChoices):
        NOT_ASSIGNED = 'Not_Assigned', ('Not_Assigned')
        WAIT_FOR_ACCEPT = 'Wait_For_Accept', _('Wait_For_Accept')
        PROCEEDING = 'Proceeding', _('Proceeding')
        COMPLETED = "Completed", _('Completed')

    type = models.CharField(
        max_length=50,
        choices=RequestType.choices)
    date_time = models.DateTimeField(auto_now=False)
    completed_date_time = models.DateTimeField(auto_now=False, null=True, blank=True)
    send_staff_id = models.ForeignKey(
        'UserApp.Staff', on_delete=models.CASCADE, blank=True, null=True, related_name="send_staff_id")
    send_guest_id = models.ForeignKey(
        'UserApp.Guest', on_delete=models.CASCADE, blank=True, null=True, related_name="send_guest_id")
    charged_staff_id = models.ForeignKey(
        'UserApp.Staff', on_delete=models.CASCADE, blank=True, null=True, related_name="charged_staff_id")
    charged_robot_id = models.ForeignKey(
        'UserApp.Robot', on_delete=models.CASCADE, blank=True, null=True, related_name="charged_robot_id")
    comment = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=50, choices=RequestStatus.choices)
    product_request_id = models.ForeignKey(
        ProductRequest, on_delete=models.CASCADE, blank=True, null=True)
    roomservice_num = models.IntegerField(blank=True, null=True)
