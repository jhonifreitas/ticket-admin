$(function(){
  var url = window.location.pathname;
  $('.sidebar .sidebar-menu [href="'+url+'"]').parent().addClass('active');

  $('.box-alerts .open').show().delay(5000).fadeOut('slow');

  $('[name="paginate_by"]').change(function(){
    location.href = '?paginate_by=' + $(this).val();
  })
});
