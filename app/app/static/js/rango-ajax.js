$(document).ready(function() {

  $('#refresh_engage').onclick(function(){
    var eid;
    alert("Yoooo")
    eid = $(this).attr("data-engagmentid");
    $.get('ajax/ajax_change_status', {enagement_id: eid}, function(data){
      $('#refesh_engage').hide();
      alert("did stuff");
    })
  });

});