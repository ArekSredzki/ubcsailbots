function getlog(){
    var pathname = window.location.pathname;
    $.get(pathname + "/getlog",function(data){
        $("#console").append(data+'<br/>');
        console.log(data);
    }
);
}
setInterval('getlog()',1000);
