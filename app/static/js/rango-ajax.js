$(document).jquery(function() {

  $('#refresh_engage').onclick(function(){
    alert("yo");
    var eid;
    eid = $(this).attr("data-engagmentid");
    $.get('ajax/ajax_change_status', {enagement_id: eid}, function(data){
      $('#refesh_engage').hide();
      alert("did stuff");
    })
  });

});