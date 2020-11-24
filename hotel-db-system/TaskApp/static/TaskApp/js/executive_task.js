
//transfer data//
$('.drag-item').on('dragstart', function(e) {
    e.originalEvent.dataTransfer.setData('listItem', $(this).index())
    console.log('starting')
  })
  
//requests//
$('.kanban-column-requests')
.on('drop', function(e) {
  e.preventDefault();
  console.log('Dropped!');
  $(this).removeClass('drop-zone-active');

  let listItemIndex = e.originalEvent.dataTransfer.getData('listItem');
  console.log(listItemIndex)
  $(this).append($('.drag-item').eq(listItemIndex))
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
    console.log(listItemIndex)
    $(this).append($('.drag-item').eq(listItemIndex))
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
    $(this).append($('.drag-item').eq(listItemIndex))
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