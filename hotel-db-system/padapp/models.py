from django.db import models

# Create your models here.
# roomservice, dnd, turn_down. complain
from RoomApp.models import Room

class Pad(models.Model):
    room = models.OneToOneField(Room, on_delete=models.CASCADE, related_name='pad_of_room')
    
class RoomService(models.Model):
    # pasta&sandwiches, FROM the grill, dessert
    TYPE_CHOICES=(
        ('PNS','PASTAS & SANDWICHES'),
        ('GRILL', 'FROM THE GRILL'),
        ('DES', 'DESSERT'),
    )

    pad = models.ForeignKey(Pad, on_delete=models.CASCADE)
    is_roomservice = models.BooleanField(default=False)
    roomservice_type = models.CharField(
        max_length='',
        choices = TYPE_CHOICES,
    )
    menu_name = models.CharField()
    price = models.DecimalField(max_digits=2, decimal_places=2)


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