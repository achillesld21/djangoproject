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

            $.ajax({
                url: "http://0.0.0.0:8000/get_user_from_token/",
                type: 'GET',
                beforeSend: function (xhr) {
                  xhr.setRequestHeader('X-CSRFToken', getCSRFToken());
                },
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
                success: function (data) {
                  $("a#user").html(data.user_name);
                    
                },
                cache: false,
                contentType: false,
                processData: false
            });
        });