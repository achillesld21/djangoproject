$(document).ready(function() {

    $("form#loginData").submit(function(e) {
        e.preventDefault();    
        var formData = new FormData(this);
    
        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: formData,
            success: function (data) {
              
                localStorage.setItem('token', data.access_token);
                localStorage.setItem('refresh', data.refresh_token);
                window.location = "http://0.0.0.0:8000/"                    
                
            },
            cache: false,
            contentType: false,
            processData: false
        });
    });
});