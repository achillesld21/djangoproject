
var post_id;
async function getData() {
    var token = localStorage.getItem('token');

    const headers = new Headers({
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
    });

    const requestOptions = {
        method: 'GET',
        headers: headers,
    };

    try {
        const web = window.location.href;
        let arr = web.split('/');
        const slug = arr[arr.length - 1];
        const res = await fetch(`http://0.0.0.0:8000/serial/${slug}`, requestOptions);
        const data = await res.json();        
        buildPage(data);
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}
function buildPage(data){
    post_id = data.id
    var usr = localStorage.getItem('user_id');
    const body = document.createElement('div');
    const container = document.querySelector('.contain');
    body.classList.add(`media-body`);
    let post_usr = data.User;
    console.log(post_usr)
    if (post_usr == usr){
        container.innerHTML =`
        <div>
      <button type="button" id="delete" class="btn btn-secondary">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-trash" viewBox="0 0 16 16">
<path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5m3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0z"></path>
<path d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4zM2.5 3h11V2h-11z"></path>
</svg>
      </button>
      </div>
      <div>
        <a href="http://0.0.0.0:8000/edit/${data.id}/" style=>
        <button type="button" class="btn btn-secondary">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-pencil-square" viewBox="0 0 16 16">
<path d="M15.502 1.94a.5.5 0 0 1 0 .706L14.459 3.69l-2-2L13.502.646a.5.5 0 0 1 .707 0l1.293 1.293zm-1.75 2.456-2-2L4.939 9.21a.5.5 0 0 0-.121.196l-.805 2.414a.25.25 0 0 0 .316.316l2.414-.805a.5.5 0 0 0 .196-.12l6.813-6.814z"></path>
<path fill-rule="evenodd" d="M1 13.5A1.5 1.5 0 0 0 2.5 15h11a1.5 1.5 0 0 0 1.5-1.5v-6a.5.5 0 0 0-1 0v6a.5.5 0 0 1-.5.5h-11a.5.5 0 0 1-.5-.5v-11a.5.5 0 0 1 .5-.5H9a.5.5 0 0 0 0-1H2.5A1.5 1.5 0 0 0 1 2.5z"></path>
</svg>
          </button>
        </a>
      </div>

        <img src="${data.image}" alt="post_image"  class="img-thumbnail" width="500">`;
    }
    else {
        container.innerHTML =`
        <img src="${data.image}" alt="post_image"  class="img-thumbnail" width="500">`
    }
   
    body.innerHTML = `
    <h5 class="mt-0">${data.heading}</h5>
    <p>${data.username}</p>
    <small>${data.posted_date}</small>
    <p class="mb-0">${data.content}</p>
    `;
    container.appendChild(body);
}

document.addEventListener('DOMContentLoaded', getData);

$(document).ready(function() {
    var token = localStorage.getItem('token');
    $(document).on('click','#delete', function(e) {
        console.log("click");
        var confirmed = window.confirm('Are you sure you want to delete this object?');
        if (confirmed) {
        console.log("click");

            $.ajax({
                url: `http://0.0.0.0:8000/deletepost/${post_id}`,
                type: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
                success: function (data) {
                    alert("blog deleted successfully");
                    window.location = "http://0.0.0.0:8000/profile";
                    
                    
                },
                cache: false,
                contentType: false,
                processData: false
            });
        }
    });
});