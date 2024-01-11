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
        const res = await fetch('http://0.0.0.0:8000/serial', requestOptions);
        const datas = await res.json();

        datas.forEach((data) => {
            buildPage(data);
        });
    } catch (error) {
        console.error('Error fetching data:', error);
    }
  }

function buildPage(data){
    const card = document.createElement('div');
    const container = document.querySelector('.contain');

    card.classList.add(`card`);
    card.innerHTML = `
    <a href="posts/${data.slug}" style="text-decoration:none" >
    <div class="card__header">
      <img src="${data.image}" alt="card__image"  class="card__image" width="600">
    </div>
    <div class="card__body">
      <span class="tag tag-blue">${data.category}</span>
      <h4>${data.heading}</h4>
    </div>
    <div class="card__footer">
      <div class="user">
        <div class="user__info">
          <h5>${data.username}</h5>
          <small>${data.posted_date}</small>
        </div>
      </div>
    </div>
    </a>`;
  
    container.appendChild(card);
}


document.addEventListener('DOMContentLoaded', getData);