
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

   