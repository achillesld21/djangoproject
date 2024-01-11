$(document).ready(function() {

    $("form#data").submit(function(e) {
        e.preventDefault(); 
        var token = localStorage.getItem('token');   
        var formData = new FormData(this);
    
        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            data: formData,
            headers: {
                'Authorization': `Bearer ${token}`,
            },
            success: function (data) {
                alert("Blog added successfully");
                window.location = "http://0.0.0.0:8000/";
                
                
            },
            cache: false,
            contentType: false,
            processData: false
        });
    });
});