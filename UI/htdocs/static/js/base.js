var containerWidth = $('#navigationBar ul').width();
var linksWidth = 0;
    $('#navigationBar ul').children().each(function() {
        linksWidth += $(this).width();
    });
    var linkSpacing = Math.floor((containerWidth - linksWidth) / ($('#navigationBar ul').children().length - 1));
$('#navigationBar ul li:not(:last-child)').css('margin-right', linkSpacing + "px");