$(document).ready(function() {
    namespace = '/test';
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + namespace);

    socket.on('my_response', function(data) {
        $("#time").text(data['time']);
        $("#weather").text(data['weather']);

        var traintimevalue = parseFloat(data['traintime']);

        if (traintimevalue < 15) {
            $("#traintime").css({'background-color': 'red', 'color': 'white'});
            $("#traintime").addClass("blink_text");
        } else {
            $("#traintime").css({'background-color': '#74f441', 'color': 'black'});
            $("#traintime").removeClass("blink_text");
        }

        $("#traintime").text(data['traintime']);
        $("#traintimenext").text(data['traintimenext']);
        $("#eur").text(data['eur']);
        $("#usd").text(data['usd']);
    });
});