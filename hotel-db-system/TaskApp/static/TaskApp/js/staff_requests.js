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
  return "룸 클리닝"
}

class RequestClass {
  constructor(request){
    this.request = request;
  }
  getItem(){
    return `<li class="drag-item" draggable="true" request_id=${this.request.id}>
    <div>요청 타입: ${getRequestTypeKor(this.request.type)}</div>
    <div>요청 시간: ${this.request.date_time}</div>
    <div>요청 고객 ID: ${this.request.send_guest_id_id}</div>
    ${this.request.status == "Proceeding" ? `<div class="cancel_btn_container">
      <button class="cancel" onClick="requestCancel(${this.request.id})">
        CANCEL
      </button>
    </div>` : ""}
    </li>`;
  }
}

function createRequestItem(request) {
  console.log(request)
  request_item = new RequestClass(request).getItem()
  console.log(`ul[name=${request.status}]`)
  $(`ul[name=${request.status}]`).append(request_item)
}

$.ajax({
  url : "/TaskApp/get_staff_requests/",
  type: "POST",
  dataType: "json",
  data : JSON.stringify({csrfmiddlewaretoken: '{{ csrf_token }}', staff_id:'101'}),
  success:function(data){
    data.requests.forEach(request => {createRequestItem(request)});
    //transfer data//
    $('.drag-item').on('dragstart', function(e) {
      e.originalEvent.dataTransfer.setData('listItem', $(this).index())
      console.log('starting')
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
  console.log('Dropped!');
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
    console.log('Dropped!');
    $(this).removeClass('drop-zone-active');
  
    let listItemIndex = e.originalEvent.dataTransfer.getData('listItem');
    $.ajax({
      url : "/TaskApp/accept/",
      type: "POST",
      dataType: "json",
      data : JSON.stringify({
        csrfmiddlewaretoken: '{{ csrf_token }}',
        request_id: $('.drag-item').eq(listItemIndex).attr('request_id')
      }),
      success:function(){
        console.log("success")
      }
    });
    let item = $('.drag-item').eq(listItemIndex)
    let request_id = item.attr('request_id')
    item.append(`<div class="cancel_btn_container">
    <button class="cancel" onClick="requestCancel(${request_id})">
      CANCEL
    </button>
  </div>`)
    $(this).children('.drag-inner-list').append(item)
    $('.drag-item').on('dragstart', function(e) {
      e.originalEvent.dataTransfer.setData('listItem', $(this).index())
      console.log('starting')
    })
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
    console.log('Dropped!');
    $(this).removeClass('drop-zone-active');
  
    let listItemIndex = e.originalEvent.dataTransfer.getData('listItem');
    console.log(listItemIndex)
    $.ajax({
      url : "/TaskApp/complete/",
      type: "POST",
      dataType: "json",
      data : JSON.stringify({
        csrfmiddlewaretoken: '{{ csrf_token }}',
        request_id: $('.drag-item').eq(listItemIndex).attr('request_id')
      }),
      success:function(){
        console.log("success")
      }
    });
    $(this).children('.drag-inner-list').append($('.drag-item').eq(listItemIndex))
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

   //side bar//
$(document).ready(function(){	
  

$('#toggleMenu .list').click(function(){
	$('#sidebar-menu li span').animate({'opacity':1, 'margin-left':'0px'});
	$('#sidebar-menu').toggleClass('animate');
	$('#toggleMenu .list').fadeOut();
	$('#toggleMenu .thumbs').fadeIn();

});

$('#toggleMenu .thumbs').click(function(){
	$('#sidebar-menu li span').css({'opacity': 0, 'margin-left': "10px"});
	$('#sidebar-menu').toggleClass('animate');	
	$('#toggleMenu .thumbs').fadeOut();
	$('#toggleMenu .list').fadeIn();	
	
});

$("#sidebar-menu li").click(function(){
	$("#sidebar-menu li").not(this).removeClass("selected");
	$(this).toggleClass("selected");
});

});