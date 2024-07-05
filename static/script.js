$(document).ready(function() {
    $('#tapButton').click(function() {
        $.ajax({
            type: 'POST',
            url: '/tap',
            success: function(data) {
                $('#counter').text(data.counter);
            }
        });
    });

    $('#resetButton').click(function() {
        $.ajax({
            type: 'POST',
            url: '/reset',
            success: function(data) {
                $('#counter').text(data.counter);
            }
        });
    });
});
