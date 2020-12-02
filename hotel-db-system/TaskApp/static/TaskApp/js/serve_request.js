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

  
  $('.kanban-column-robot1')
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

     
  $('.kanban-column-robot2')
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

   $('.kanban-column-robot3')
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
 
      
   $('.kanban-column-robot4')
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