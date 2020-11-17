from django.db import models

# Create your models here.


class Guest(models.Model):
    objects = models.Manager()
    is_guest = models.BooleanField(default=True)
    site_id = models.CharField(max_length=20)
    site_pw = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nation = models.CharField(max_length=40, null=True)
    gender = models.CharField(max_length=1, null=True)
    email = models.CharField(max_length=40, null=True)
    birthday = models.DateField(null=True)
    reseve_num = models.IntegerField(null=True)
    car_num = models.IntegerField(null=True)
    is_pad = models.BooleanField(default=True, null=True)
    car_cvc_num = models.IntegerField(null=True)
    card_experiment = models.IntegerField(null=True)
    car_password = models.IntegerField(null=True)
    room_person_cnt = models.IntegerField(null=True)
    room_type = models.CharField(max_length=20, null=True)
    check_in = models.DateTimeField(null=True)
    check_out = models.DateTimeField(null=True)
    room_service_fee = models.IntegerField(null=True)
    guest_point = models.IntegerField(null=True)

    class Meta:
        db_table = 'guest'


class Staff(models.Model):
    objects = models.Manager()
    department = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nation = models.CharField(max_length=40)
    gender = models.CharField(max_length=1)
    birthday = models.DateField()
    email = models.CharField(max_length=40)
    phone_number = models.CharField(max_length=50)
    hire_date = models.DateField()
    salary = models.IntegerField()
    position = models.CharField(max_length=100)

    class Meta:
        db_table = 'staff'


class Sales(models.Model):
    date = models.DateTimeField()
    fee = models.IntegerField()
    payment_num = models.IntegerField()

    class Meta:
        db_table = 'sales'
