from django.db import models

# Create your models here.


class Guest(models.Model):
    objects = models.Manager()
    is_guest = models.BooleanField(default=True)
    site_id = models.CharField(max_length=20)
    site_pw = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nation = models.CharField(max_length=40, null=True, blank=True)
    gender = models.CharField(max_length=1, null=True, blank=True)
    email = models.CharField(max_length=40, null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    reserve_num = models.ForeignKey('RoomApp.Booking', on_delete=models.SET_NULL, null=True, blank=True)
    car_num = models.IntegerField(null=True, blank=True)
    is_pad = models.BooleanField(default=True, null=True, blank=True)
    card_cvc_num = models.IntegerField(null=True, blank=True)
    card_experiment = models.IntegerField(null=True, blank=True)
    card_password = models.IntegerField(null=True, blank=True)
    room_person_cnt = models.IntegerField(null=True, blank=True)
    room_type = models.CharField(max_length=20, null=True, blank=True)
    check_in = models.DateTimeField(null=True, blank=True)
    check_out = models.DateTimeField(null=True, blank=True)
    room_service_fee = models.IntegerField(null=True, blank=True)
    guest_point = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'ID: {self.site_id} NAME: {self.first_name} {self.last_name}'

    class Meta:
        db_table = 'guest'


class Staff(models.Model):
    objects = models.Manager()
    staff_id = models.IntegerField(default=0)
    department_type = (('Cleaning Dept', 'Cleaning Dept'),
                       ('Food Beverage Dept', 'Food Beverage Dept'),
                       ('Front Office Dept', 'Front Office Dept'),
                       ('Customer Response Dept', 'Customer Response Dept'),
                       ('Technical Support Dept', 'Technical Support Dept'),
                       ('Parking Dept', 'Parking Department'),
                       ('Purchasing Dept', 'Purchasing Department'),
                       ('Center', 'Center Department'),
                       ('Executive', 'Executive'))
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    nation = models.CharField(max_length=40, null=True, blank=True)
    gender_type = (('MALE', 'Male'),
                   ('FEMALE', 'Female'),)
    gender = models.CharField(
        max_length=6, choices=gender_type, default="Male")
    birthday = models.DateField(null=True, blank=True)
    email = models.CharField(max_length=40, null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    salary = models.IntegerField(null=True, blank=True)
    position = models.CharField(max_length=100, null=True, blank=True)
    had_annual_leave = models.IntegerField(default=0)
    department = models.CharField(
        max_length=25, choices=department_type, default="None")

    def __str__(self):
        return f'ID: {self.staff_id} NAME: {self.first_name} {self.last_name} DEPARTMENT: {self.department}'

    class Meta:
        db_table = 'staff'


class Sales(models.Model):
    objects = models.Manager()
    date = models.DateTimeField()
    fee = models.IntegerField()
    payment_num = models.IntegerField()

    def __str__(self):
        return f'DATE: {self.date} FEE: {self.fee} payment_num: {self.payment_num}'

    class Meta:
        db_table = 'sales'


class Robot(models.Model):
    objects = models.Manager()
    work_check = models.BooleanField(default=False)
    is_emergency = models.BooleanField(default=False)
    position = models.CharField(max_length=50)

    def __str__(self):
        return f'work_check: {self.work_check} is_emergency: {self.is_emergency} position: {self.position}'


class Attendance(models.Model):
    objects = models.Manager()
    staff_id = models.ForeignKey(
        'Staff', on_delete=models.CASCADE, db_column='staff_id')
    date = models.DateTimeField(null=True)
    start_time = models.DateTimeField(null=True)
    finish_time = models.DateTimeField(null=True)
    work_type = models.CharField(max_length=50, null=True)
    description = models.TextField(null=True)
    accept = models.BooleanField(null=True)


class StaffLeave(models.Model):
    objects = models.Manager()
    staff_id = models.ForeignKey(
        'Staff', on_delete=models.CASCADE, db_column='staff_id')
    start_time = models.DateField()
    finish_time = models.DateField()
    accept = models.BooleanField(default=False)
