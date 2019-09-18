$(function(){
  url = window.location.pathname;
  $('.sidebar .sidebar-menu [href="'+url+'"]').parent().addClass('active');

  $('.box-alerts .open').show().delay(5000).fadeOut('slow');
});
