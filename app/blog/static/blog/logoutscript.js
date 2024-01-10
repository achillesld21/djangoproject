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
    var token = localStorage.getItem('token');
    $(document).on('click','#logout', function(e) {
        var confirmed = window.confirm('Are you sure you want to logout?');
        if (confirmed) {
        console.log("click");

            $.ajax({
                url: "http://0.0.0.0:8000/login/api/logout/",
                type: 'GET',
                beforeSend: function (xhr) {
                  xhr.setRequestHeader('X-CSRFToken', getCSRFToken());
                },
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
                success: function (data) {
                    localStorage.removeItem('refresh');
                    localStorage.removeItem('token');
                    alert("logout successfull");
                    window.location = "http://0.0.0.0:8000/login/login_user";
                    
                },
                cache: false,
                contentType: false,
                processData: false
            });
        }
    });
});