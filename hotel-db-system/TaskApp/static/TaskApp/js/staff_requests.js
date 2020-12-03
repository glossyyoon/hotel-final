function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
          var cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
  // these HTTP methods do not require CSRF protection
  return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
  beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
          xhr.setRequestHeader("X-CSRFToken", csrftoken);
      }
  }
});

function getRequestTypeKor(type){
  if(type == 'Room_Service')
    return "룸 서비스"
  return "룸 기타 컴플레인"
}

class RequestClass {
  constructor(request){
    this.request = request;
  }
  getDateFormat(date){
    console.log(date)
    date = new Date(date)
    return (date.getMonth()+1) + "월 " + date.getDate() + "일 " + date.getHours() + "시 " + date.getMinutes() + "분 " + date.getSeconds() + "초";
  }
  getMenuList(){
    var list = ``
    this.request.roomservice_list.forEach(roomservice => {
      list += `<li>${roomservice.menu}    x ${roomservice.count}</li>`
    });
    return list;
  }
  getItem(){
    return `<li class="drag-item" draggable="true" request_id=${this.request.id}>
    <div class="request-info-container">
    <div>요청 타입: ${getRequestTypeKor(this.request.type)}</div>
    <div>요청 시간: ${this.getDateFormat(this.request.date_time)}</div>
    <div class="complete_time" style="display:${this.request.status !== "Completed" ? 'none;' : 'block;'}">완료 시간: ${this.getDateFormat(this.request.completed_date_time)}</div>
    <div>요청 고객 ID: ${this.request.send_guest_id_id}</div>
    <div>요청 룸 ID: ${this.request.room_id}</div>
    ${this.request.type === "Room_Service" ?
    `<ul>요청 메뉴 리스트:${this.getMenuList()}</ul>`
    : "" }
    <div>요청 코멘트: ${this.request.comment}</div>
    ${this.request.status !== "Completed" ? 
    `<div class="cancel_btn_container">
      <button class="cancel" onClick="requestCancel(${this.request.id})">
      CANCEL
      </button>
    </div>` : ""}
    </div>
    </li>`;
  }
}

function createRequestItem(request) {
  request_item = new RequestClass(request).getItem()
  $(`ul[name=${request.status}]`).append(request_item)
}

$.ajax({
  url : "/TaskApp/getStaffID/",
  type: "POST",
  dataType: "json",
  data : JSON.stringify({csrfmiddlewaretoken: '{{ csrf_token }}'}),
  success:function(data){
    console.log(data)
    $.ajax({
    url : "/TaskApp/get_staff_requests/",
    type: "POST",
    dataType: "json",
    data : JSON.stringify({csrfmiddlewaretoken: '{{ csrf_token }}', staff_id: data.staff_id}),
    success:function(data){
      data.requests.forEach(request => {createRequestItem(request)});
      //transfer data//
      $('.drag-item').on('dragstart', function(e) {
        e.originalEvent.dataTransfer.setData('listItem', $(this).attr('request_id'))
      })
    }
  })
  }
});

function requestCancel(request_id){

  $(`li[request_id=${request_id}]`).remove()
  $.ajax({
    url : "/TaskApp/cancel/",
    type: "POST",
    dataType: "json",
    data : JSON.stringify({csrfmiddlewaretoken: '{{ csrf_token }}', request_id: request_id}),
    success:function(){
      console.log("request cancel success")
    }
  });
}
  
//requests//
$('.kanban-column-requests')
.on('drop', function(e) {
  e.preventDefault();
  $(this).removeClass('drop-zone-active');
})
.on('dragover', function(e) {
   e.preventDefault();
 })
 .on('dragenter', function(e) {
   $(this).addClass('drop-zone-active');
 })
 .on('dragleave', function(e) {
   $(this).removeClass('drop-zone-active')
 })

  //progress//
  $('.kanban-column-progress')
  .on('drop', function(e) {
    e.preventDefault();
    $(this).removeClass('drop-zone-active');
  
    let listItemRequestID= e.originalEvent.dataTransfer.getData('listItem');
    let item = $(`[request_id=${listItemRequestID}]`)
    let request_id = item.attr('request_id')
    $.ajax({
      url : "/TaskApp/accept/",
      type: "POST",
      dataType: "json",
      data : JSON.stringify({
        csrfmiddlewaretoken: '{{ csrf_token }}',
        request_id: request_id
      }),
      success:function(){
        console.log("success")
      }
    });
    if(item.find($('.cancel_btn_container')).length === 0)
      item.append(`<div class="cancel_btn_container">
      <button class="cancel" onClick="requestCancel(${request_id})">
        CANCEL
      </button>
    </div>`)
    $(this).children('.drag-inner-list').append(item)
  })
  .on('dragover', function(e) {
     e.preventDefault();
   })
   .on('dragenter', function(e) {
     $(this).addClass('drop-zone-active');
   })
   .on('dragleave', function(e) {
     $(this).removeClass('drop-zone-active')
   })

     //done//
  $('.kanban-column-done')
  .on('drop', function(e) {
    e.preventDefault();
    $(this).removeClass('drop-zone-active');
  
    let listItemRequestID = e.originalEvent.dataTransfer.getData('listItem');
    let item = $(`[request_id=${listItemRequestID}]`)
    let request_id = item.attr('request_id')
    $.ajax({
      url : "/TaskApp/complete/",
      type: "POST",
      dataType: "json",
      data : JSON.stringify({
        csrfmiddlewaretoken: '{{ csrf_token }}',
        request_id: request_id
      }),
      success:function(){
        console.log("success")
      }
    });
    item.find($('.complete_time'))[0].style.display = 'block'
    if(item.find($('.cancel_btn_container')).length === 1)
      item.find($('.cancel_btn_container'))[0].remove()
    $(this).children('.drag-inner-list').append(item)
  })
  .on('dragover', function(e) {
     e.preventDefault();
   })
   .on('dragenter', function(e) {
     $(this).addClass('drop-zone-active');
   })
   .on('dragleave', function(e) {
     $(this).removeClass('drop-zone-active')
   })

   var menuBtn = document.querySelector('.menu-btn');
   var nav = document.querySelector('nav');
   var lineOne = document.querySelector('nav .menu-btn .line--1');
   var lineTwo = document.querySelector('nav .menu-btn .line--2');
   var lineThree = document.querySelector('nav .menu-btn .line--3');
   var link = document.querySelector('nav .nav-links');
   menuBtn.addEventListener('click', () => {
       nav.classList.toggle('nav-open');
       lineOne.classList.toggle('line-cross');
       lineTwo.classList.toggle('line-fade-out');
       lineThree.classList.toggle('line-cross');
       link.classList.toggle('fade-in');
   })