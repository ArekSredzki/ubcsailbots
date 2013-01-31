function getlog(){
    var pathname = window.location.pathname;
    
    $.ajax({
  		url: window.location.pathname + '/getlog',
  		type: 'GET',
  		dataType: "text",
  		success: function (data) {
        $("#console").append(data+'<br/>');
        console.log(data);
  		}
	});
}
setInterval('getlog()',1000);
