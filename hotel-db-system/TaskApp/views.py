from enum import Enum

from django.core.cache import cache
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import Q
from datetime import datetime
from UserApp.models import Guest

from .models import Request, ProductRequest
from .place import Coordinate, get_place_coord, get_distance, convert_to_coordinate

# 요청 거절
REJECTED = 1
# 요청 아직 선택안함
NOT_YET = 0

class Department(Enum):
    CLEANING = "Cleaning Dept"
    BEVERAGE = "Beverage Dept"
    FRONT_OFFICE = "Front office Dept"
    ROBOT = "Robot"
    PARKING = "Parking Dept"
    PURCHASING = "Purchasing Dept"
    CENTER = "Center Dept"

def request_send(req, type, send_user_id):
    request = None
    send_guest_id = None
    send_staff_id = None
    comment = req.POST['comment'] if (req.POST in 'comment') else None
    product_request_id = None
    if type in [
        Request.RequestType.ROOM_CLEANING,
        Request.RequestType.ROOM_SERVICE,
        Request.RequestType.ROOM_ERROR,
        Request.RequestType.ROOM_ETC,
        Request.RequestType.CARRY_IN,
        Request.RequestType.CARRY_OUT,
        Request.RequestType.VALET_PARKING,
        Request.RequestType.CARRY_ROOM_SERVICE,]:
        send_guest_id = send_user_id
    elif type == Request.RequestType.PRODUCT_PURCHASING:
        send_staff_id = send_user_id
        try:
            product_request_id = req.POST['product_request_id']
        except (KeyError, ProductRequest.DoesNotExist):
            render(request, '', {
                'error_message': "product_request_id 값이 존재하지 않습니다."
            })
    elif type == Request.RequestType.ETC:
        send_staff_id = send_user_id
    request = Request.objects.create(
        type=type,
        send_staff_id=send_staff_id,
        send_guest_id=send_guest_id,
        comment=comment,
        product_request_id=product_request_id,
        status=Request.RequestStatus.NOT_ASSIGNED
    )
    return render(request, '', {"request_id": request.id}, status=201)

def request_convey(request):
    request.charged_staff_id = get_optimal_request_charger_list(request)[0]
    request.status = Request.RequestStatus.WAIT_FOR_ACCEPT
    request.save()

def request_assign(req):
    try:
        request = Request.objects.get(pk=req.POST["request_id"])
        request.charged_staff_id = req.POST["request_id"]
        request.status = Request.RequestStatus.WAIT_FOR_ACCEPT
        request.save()
    except Request.DoesNotExist:
        return render(req, '', {"error_message": "존재하지 않는 요청 정보입니다."}, status=400)
    except Staff.DoesNotExist:
        return render(req, '', {"error_message": "존재하지 않는 직원 정보입니다."}, status=400)
    else:
        return render(req, '', status=200)

def request_get_department_in_charge(request):
    if request.type == Request.RequestType.ROOM_CLEANING:
        return Department.CLEANING
    elif request.type == Request.RequestType.ROOM_SERVICE:
        return Department.BEVERAGE
    elif request.type in [
        Request.RequestType.ROOM_ERROR,
        Request.RequestType.ROOM_ETC,]:
        return Department.FRONT_OFFICE
    elif request.type in [
        Request.RequestType.CARRY_IN,
        Request.RequestType.CARRY_OUT,
        Request.RequestType.CARRY_ROOM_SERVICE]:
        return Department.ROBOT
    elif request.type == Request.RequestType.VALET_PARKING:
        return Department.PARKING
    elif request.type == Request.RequestType.PRODUCT_PURCHASING:
        return Department.PURCHASING
    elif request.type == Request.RequestType.ETC:
        return Department.CENTER

def request_get_coordinate(request):
    if request.type in [
        Request.RequestType.ROOM_CLEANING,
        Request.RequestType.ROOM_ERROR,
        Request.RequestType.ROOM_ETC,
        Request.RequestType.CARRY_ROOM_SERVICE,]:
        try:
            guest = Guest.objects.get(pk=request.send_guest_id)
        except Guest.DoesNotExist:
            print("게스트 정보를 불러오는데에 실패하였습니다.")
            return None
        try:
            reserve = Reserve.objects.get(pk=guest.reserve_num)
        except Reserve.DoesNotExist:
            print("룸 예약 정보를 불러오는데에 실패하였습니다.")
            return None
        return get_place_coord("R" + reserve.room_id)
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

def get_optimal_request_charger_list(request):
    department = request_get_department_in_charge(request)
    request_coord = request_get_coordinate(request)
    if department == Department.ROBOT:
        charger_list = Robot.objects.filter(work_check=False)
        return sorted(charger_list,
        lambda robot: (
            robot.task_count,
            get_distance(request_coord, convert_to_coordinate(robot.position))))
    else:
        charger_list = Staff.objects.filter(department=department)
        charger_list = list(filter(lambda charger: cache.get((charger.staff_id, request.id), NOT_YET) == REJECTED, charger_list))
        return sorted(charger_list,
        lambda staff: (
            staff.task_count,
            get_distance(request_coord, convert_to_coordinate(staff.position))))

def request_accept(req):
    try:
        request = Request.objects.get(pk=req.POST["request_id"])
        staff = Staff.objects.get(pk=req.POST["staff_id"])
        staff.task_count = staff.task_count + 1
        request.charged_staff_id = staff.id
        request.status = Request.RequestStatus.PROCEEDING
    except (KeyError, Request.DoesNotExist):
        return render(req, '', status=400)
    except Staff.DoesNotExist:
        return render(req, '', {"error_message": "존재하지 않는 직원 정보입니다."}, status=400)
    else:
        request.save()
        return render(req, '', status=200)

def request_reject(req):
    try:
        request = Request.objects.get(pk=req.POST["request_id"], charged_staff_id=req.POST["charged_staff_id"])
    except (KeyError, Request.DoesNotExist):
        return render(req, '', status=400)
    else:
        cache.set((req.POST["charged_staff_id"], req.POST["request_id"]), REJECTED, 60 * 60)
        request.charged_staff_id = None
        request.status = Request.RequestStatus.NOT_ASSIGNED
        request.save()
        request_convey(request)
        return render(req, '', status=200)

def request_complete(req):
    try:
        request = Request.objects.get(pk=req.POST["request_id"])
        staff = Staff.objects.get(pk=req.POST["staff_id"])
        staff.task_count = staff.task_count - 1
        request.status = Request.RequestStatus.COMPLETED
        request.save()
        staff.save()
    except (KeyError, Request.DoesNotExist, Staff.DoesNotExist):
        return render(req, '', status=400)
    else:
        return render(req, '', status=200)

def request_cancel(req):
    try:
        request = Request.objects.get(pk=req.POST["request_id"])
        staff = Staff.objects.get(pk=req.POST["staff_id"])
        staff.task_count = staff.task_count - 1
        cache.set((request.charged_staff_id, req.POST["request_id"]), REJECTED, 60 * 60)
        request.charged_staff_id = None
        request.status = Request.RequestStatus.NOT_ASSIGNED
        request.save()
        request_convey(request)
        staff.save()
    except (KeyError, Request.DoesNotExist, Staff.DoesNotExist):
        return render(req, '', status=400)
    else:
        return render(req, '', status=200)

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
    return render(req, '', {"requests_list": requests_list}, status=200)