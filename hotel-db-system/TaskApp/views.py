from enum import Enum
import json
from django.utils import timezone

from django.core.cache import cache
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.views import generic

from UserApp.models import Guest
from .models import Request, ProductRequest
from .place import Coordinate, get_place_coord, get_distance, convert_to_coordinate
from RoomApp.models import Room, Booking
from PadApp.models import RoomService, RoomServiceType, Pad
from UserApp.models import Guest, Staff, Robot

# 요청 거절
REJECTED = 1
# 요청 아직 선택안함
NOT_YET = 0

class Department(Enum):
    CLEANING = "Cleaning Dept"
    FOOD_BEVERAGE = "Food Beverage Dept"
    FRONT_OFFICE = "Front Office Dept"
    CUSTOMER_RESPONSE = "Customer Response Dept"
    TECHNICAL_SUPPORT = "Technical Support Dept"
    ROBOT = "Robot"
    PARKING = "Parking Dept"
    PURCHASING = "Purchasing Dept"
    CENTER = "Center Dept"

class StaffRequestsView(generic.ListView):
    model = Request
    template_name = 'TaskApp/staff_requests.html'

def get_staff_requests(req):
    json_data = json.loads(req.body)
    staff = Staff.objects.get(staff_id=json_data["staff_id"])
    request_list = Request.objects.filter(charged_staff_id=staff.pk).values()
    for request in request_list:
        if request['type'] in [
        Request.RequestType.ROOM_CLEANING,
        Request.RequestType.ROOM_SERVICE,
        Request.RequestType.ROOM_ERROR,
        Request.RequestType.ROOM_ETC]:
            guest = Guest.objects.get(pk=request['send_guest_id_id'])
            booking = Booking.objects.get(pk=guest.reserve_num_id)
            request['room_id'] = booking.booking_roomid.room_id
        if request['type'] == Request.RequestType.ROOM_SERVICE:
            roomservice_request_list = RoomService.objects.filter(roomservice_num=request['roomservice_num']).values()
            roomservice_name_count_list = []
            for roomservice_request in roomservice_request_list:
                roomservice = RoomServiceType.objects.get(pk=roomservice_request['select_roomservice_id'])
                roomservice_name_count_list.append({'menu': roomservice.menu_name, 'count': roomservice_request['count']})
            request['roomservice_list'] = roomservice_name_count_list
    return JsonResponse({'requests': list(request_list)}, status=201)

def request_send(req):
    send_guest_id = req.POST['send_guest_id'] if (req.POST in 'send_guest_id') else None
    send_staff_id = req.POST['send_staff_id'] if (req.POST in 'send_staff_id') else None
    comment = req.POST['comment'] if (req.POST in 'comment') else None
    product_request_id = req.POST['product_request_id'] if (req.POST in 'product_request_id') else None
    roomservice_num = req.POST['roomservice_num'] if (req.POST in 'roomservice_num') else None
    if roomservice_num != None:
        roomservice_pad = req.POST['pad_id']
        roomservice_requests = RoomService.objects.filter(roomservice_num = roomservice_num)
        roomservice_room = Pad.objects.get(pk=roomservice_pad).pad_room
        booking = Booking.objects.filter(booking_roomid=roomservice_room, checkIn__gte=timezone.now(), checkOut__lte=timezone.now())
        send_guest_id = booking.booking_userid

    request = Request.objects.create(
        type=type,
        date_time=timezone.now(),
        send_staff_id=send_staff_id,
        send_guest_id=send_guest_id,
        comment=comment,
        product_request_id=product_request_id,
        roomservice_num=roomservice_num,
        status=Request.RequestStatus.NOT_ASSIGNED
    )
    request_convey(request)
    return JsonResponse({"request_id": request.id}, status=201)

def request_convey(request):
    optimal_charger_list = get_optimal_request_charger_list(request)
    if len(optimal_charger_list) == 0:
        return
    optimal_charger = optimal_charger_list[0]
    if isinstance(optimal_charger, Staff):
        request.charged_staff_id = optimal_charger
    request.status = Request.RequestStatus.WAIT_FOR_ACCEPT
    request.save()

def request_assign_optimal(request):
    optimal_charger_list = get_optimal_request_charger_list(request)
    if len(optimal_charger_list) == 0:
        return
    optimal_charger = optimal_charger_list[0]
    if isinstance(optimal_charger, Staff):
        request.charged_staff_id = optimal_charger
    else:
        request.charged_robot_id = optimal_charger
        robot = Robot.objects.get(pk=optimal_charger.id)
        robot.work_check = True
        robot.save()
    request.status = Request.RequestStatus.PROCEEDING
    request.save()

def request_assign(req):
    try:
        request = Request.objects.get(pk=req.POST["request_id"])
        request.charged_staff_id = req.POST["request_id"]
        request.status = Request.RequestStatus.WAIT_FOR_ACCEPT
        request.save()
    except Request.DoesNotExist:
        return JsonResponse(data={"error_message": "존재하지 않는 요청 정보입니다."}, status=400)
    except Staff.DoesNotExist:
        return JsonResponse(data={"error_message": "존재하지 않는 직원 정보입니다."}, status=400)
    else:
        return HttpResponse(status=200)

def request_get_department_in_charge(request):
    if request.type == Request.RequestType.ROOM_CLEANING:
        return Department.CLEANING.value
    elif request.type == Request.RequestType.ROOM_SERVICE:
        return Department.FOOD_BEVERAGE.value
    elif request.type in [
        Request.RequestType.ROOM_ERROR,
        Request.RequestType.ROOM_ETC,]:
        return Department.FRONT_OFFICE.value
    elif request.type in [
        Request.RequestType.CARRY_IN,
        Request.RequestType.CARRY_OUT,
        Request.RequestType.CARRY_ROOM_SERVICE]:
        return Department.ROBOT.value
    elif request.type == Request.RequestType.VALET_PARKING:
        return Department.PARKING.value
    elif request.type == Request.RequestType.PRODUCT_PURCHASING:
        return Department.PURCHASING.value
    elif request.type == Request.RequestType.ETC:
        return Department.CENTER.value

def request_get_coordinate(request):
    if request.type in [
        Request.RequestType.ROOM_CLEANING,
        Request.RequestType.ROOM_ERROR,
        Request.RequestType.ROOM_ETC,]:
        guest = Guest.objects.get(pk=request.send_guest_id_id)
        booking = Booking.objects.get(pk=guest.reserve_num_id)
        room = Room.objects.get(pk=booking.booking_roomid_id)
        return get_place_coord("R" + str(room.room_id))
    elif request.type in [
        Request.RequestType.ROOM_SERVICE,
        Request.RequestType.CARRY_ROOM_SERVICE,]:
        return get_place_coord("Kitchen")
    elif request.type == Request.RequestType.CARRY_IN:
        return get_place_coord("Front")
    elif request.type == Request.RequestType.VALET_PARKING:
        try:
            guest = Guest.objects.get(pk=request.send_guest_id)
        except Guest.DoesNotExist:
            print("게스트 정보를 불러오는데에 실패하였습니다.")
            return None
        return get_place_coord("P" + guest.parking_floor)
    elif request.type == Request.RequestType.PRODUCT_PURCHASING:
        return get_place_coord("Purchasing")
    elif request.type == Request.RequestType.ETC:
        return get_place_coord("Center")
    else:
        return Coordinate(0, 0, 0)

def get_optimal_request_charger_list(request):
    department = request_get_department_in_charge(request)
    request_coord = request_get_coordinate(request)
    if department == Department.ROBOT.value:
        charger_list = Robot.objects.filter(work_check=False)
        return sorted(charger_list,
        key=lambda robot: (
            len(Request.objects.filter(charged_robot_id=robot.id)),
            get_distance(request_coord, convert_to_coordinate(robot.position))))
    else:
        charger_list = Staff.objects.filter(department=department)
        # charger_list = list(filter(lambda charger: cache.get((charger.staff_id, request.id), NOT_YET) == REJECTED, charger_list))
        return sorted(charger_list,
        key=lambda staff: (
            len(Request.objects.filter(charged_staff_id=staff.staff_id)),
            get_distance(request_coord, convert_to_coordinate(staff.position))))

def request_accept(req):
    try:
        json_data = json.loads(req.body)
        request = Request.objects.get(pk=json_data["request_id"])
        request.status = Request.RequestStatus.PROCEEDING
    except (KeyError, Request.DoesNotExist):
        return JsonResponse(data={"error_message": "존재하지 않는 요청이거나, http 요청 property가 존재하지 않습니다."}, status=400)
    else:
        request.save()
        return HttpResponse(status=200)

def request_reject(req):
    try:
        request = Request.objects.get(pk=req.POST["request_id"], charged_staff_id=req.POST["charged_staff_id"])
    except (KeyError, Request.DoesNotExist):
        return JsonResponse(data={"error_message": "존재하지 않는 요청이거나, http 요청 property가 존재하지 않습니다."}, status=400)
    else:
        cache.set((req.POST["charged_staff_id"], req.POST["request_id"]), REJECTED, 60 * 60)
        request.charged_staff_id = None
        request.status = Request.RequestStatus.NOT_ASSIGNED
        request.save()
        request_convey(request)
        return HttpResponse(status=200)

def request_complete(req):
    try:
        json_data = json.loads(req.body)
        request = Request.objects.get(pk=json_data["request_id"])
        guest = Guest.objects.get(pk=request.send_guest_id_id)
        request.status = Request.RequestStatus.COMPLETED
        request.completed_date_time = timezone.now()
        request.save()
        if request.type == Request.RequestType.ROOM_SERVICE:
            request = Request.objects.create(
            type=Request.RequestType.CARRY_ROOM_SERVICE,
            date_time=timezone.now(),
            send_guest_id=guest,
            comment=request.comment,
            status=Request.RequestStatus.NOT_ASSIGNED
            )
            request.save()
            request_assign_optimal(request)
    except (KeyError, Request.DoesNotExist):
        return JsonResponse(data={"error_message": "존재하지 않는 요청이거나, http 요청 property가 존재하지 않습니다."}, status=400)
    else:
        return HttpResponse(status=200)

def request_cancel(req):
    try:
        json_data = json.loads(req.body)
        request = Request.objects.get(pk=json_data["request_id"])
        # cache.set((request.charged_staff_id, request.id), REJECTED, 60 * 60)
        request.charged_staff_id = None
        request.status = Request.RequestStatus.NOT_ASSIGNED
        request.save()
        request_convey(request)
    except (KeyError, Request.DoesNotExist):
        return JsonResponse(data={"error_message": "존재하지 않는 요청이거나, http 요청 property가 존재하지 않습니다."}, status=400)
    else:
        return HttpResponse(req, '', status=200)

def request_get_list(req):
    q = Q()
    if req.POST in 'type':
        q.add(Q(type=req.POST['type']))
    if req.POST in 'send_staff_id':
        q.add(Q(send_staff_id=req.POST['send_staff_id']))
    if req.POST in 'send_guest_id':
        q.add(Q(send_guest_id=req.POST['send_guest_id']))
    if req.POST in 'charged_staff_id':
        q.add(Q(charged_staff_id=req.POST['charged_staff_id']))
    if req.POST in 'charged_robot_id':
        q.add(Q(charged_robot_id=req.POST['charged_robot_id']))
    if req.POST in 'status':
        q.add(Q(status=req.POST['status']))
    if req.POST in 'from' and req.POST in 'to':
        q.add(Q(date_time__range=[req.POST['from'], req.POST['to']]))
    requests_list = Request.objects.filter(q)
    return HttpResponse(req, '', {"requests_list": requests_list}, status=200)