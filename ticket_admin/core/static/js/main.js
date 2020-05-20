$(function(){
  var url = window.location.pathname;
  $parent = $('.sidebar .sidebar-menu [href="'+url+'"]').parent();
  $parent.addClass('active');
  $parent.parents('.treeview-menu').slideDown('slow');
  $parent.parents('.treeview').addClass('menu-open');

  $('.box-alerts .open').show().delay(5000).fadeOut('slow');

  $('[name="paginate_by"]').change(function(){
    location.href = '?paginate_by=' + $(this).val();
  })
});
