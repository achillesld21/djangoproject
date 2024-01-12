function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (const cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return value;
        }
    }
    return null;
}
$(document).ready(function() {

    $("form#data").submit(function(e) {
        e.preventDefault(); 
        var token = localStorage.getItem('token');   
        var formData = new FormData(this);
    
        $.ajax({
            url: 'http://0.0.0.0:8000/login/api/register',
            type: 'POST',
            data: formData,
            beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', getCSRFToken());
              },
            success: function (data) {
                window.location = "http://0.0.0.0:8000/login/login_user";
                
                
            },
            cache: false,
            contentType: false,
            processData: false
        });
    });
});