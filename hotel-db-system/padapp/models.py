from django.db import models
from RoomApp.models import Room, Guest

class Pad(models.Model):
    pad_room = models.ForeignKey("RoomApp.Room", on_delete=models.CASCADE)
    # roomservice = models.ForeignKey(RoomService, on_delete=SET_NULL, null=True)
    # dnd = models.ForeignKey(Dnd, on_delete=SET_NULL, null=True)
    # turndown = models.ForeignKey(TurnDown, on_delete=SET_NULL, null=True)
    # compalin = models.ForeignKey(Complain, on_delete=SET_NULL, null=True)

class RoomServiceType(models.Model): #Menu
    TYPE_CHOICES=(
        ('PNS','PASTAS & SANDWICHES'),
        ('GRILL', 'FROM THE GRILL'),
        ('DES', 'DESSERT'),
    )
    menu_type = models.CharField(
            max_length=5,
            choices = TYPE_CHOICES,
        )
    menu_name = models.CharField(max_length=100)
    description = models.CharField(max_length=500, null=True)
    image = models.ImageField(blank=True, upload_to="roomservice")
    price = models.IntegerField(default=0)
    count = models.IntegerField(default=1)
    def __str__(self):
        return '%s - %s' % (self.menu_type, self.menu_name)    

class OrderItem(models.Model):
    item = models.ForeignKey(RoomServiceType, on_delete=models.CASCADE)

    def __str__(self):
        return self.menu_name

class RoomService(models.Model):
    user = models.ForeignKey(Guest, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    pad = models.ForeignKey(Pad, on_delete=models.CASCADE)
    is_roomservice = models.BooleanField(default=False)
    # select_roomservice = models.ForeignKey(RoomServiceType, on_delete=models.SET_NULL, null=True)
    count = models.IntegerField(default=1)

    # def __str__(self):
    #     return self.id

    def sub_total(self):
        return self.select_roomservice.price * self.count

class Dnd(models.Model):
    pad = models.ForeignKey(Pad, on_delete=models.CASCADE)
    is_dnd = models.BooleanField(default=False)

class TurnDown(models.Model):
    pad = models.ForeignKey(Pad, on_delete=models.CASCADE)
    is_turndown = models.BooleanField(default=False)

class Complain(models.Model):
    # 물품요청, 기계오작동, 위생불만족, 기타
    ITEMREQUEST = 'ITEM'
    MALFUNCTION = 'BD'
    SANITARY = 'SANI'
    ETC = 'ETC'

    TYPE_CHOICES = (
        (ITEMREQUEST,'물품 요청'),
        (MALFUNCTION, '기계 오작동'),
        (SANITARY, '위생 불만족'),
        (ETC, '기타'),
    )

    pad = models.ForeignKey(Pad, on_delete=models.CASCADE)
    is_complain = models.BooleanField(default=False)
    complain_type = models.CharField(
        max_length=4,
        choices=TYPE_CHOICES,
    )
    content = models.TextField(max_length=800)