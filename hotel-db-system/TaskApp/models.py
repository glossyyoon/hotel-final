from django.db import models

class ProductRequest(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    product_item = models.CharField(max_length=100)
    product_count = models.IntegerField(default=1)
    product_from = models.DateTimeField(auto_now=True)
    product_to = models.DateTimeField(auto_now=False)

class Request(models.Model):

    class RequestType(models.TextChoices):
        ROOM_CLEANING = 'Room_Cleaning'
        ROOM_SERVICE = 'Room_Service'
        ROOM_ERROR = 'Room_Error'
        ROOM_ETC = "Room_ETC"
        CARRY_IN = "Carry_In"
        CARRY_OUT = "Carry_Out"
        VALET_PARKING = "Valet_Parking"
        PRODUCT_PURCHASING = "Product_Purchasing"
        CARRY_ROOM_SERVICE = "Carry_Room_Service"
        ETC = "ETC"

    class RequestStatus(models.TextChoices):
        NOT_ASSIGNED = 'Not_Assigned'
        WAIT_FOR_ACCEPT = 'Wait_For_Accept'
        PROCEEDING = 'Proceeding'
        COMPLETED = "Completed"

    type = models.CharField(
        max_length=30,
        choices=RequestType.choices)
    date_time = models.DateTimeField(auto_now=True)
    send_staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    send_guest_id = models.ForeignKey(Guest, on_delete=models.CASCADE, null=True)
    charged_staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)
    charged_robot_id = models.ForeignKey(Robot, on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=200, null=True)
    product_request_id = models.ForeignKey(ProductRequest, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=20, choices=RequestStatus.choices)