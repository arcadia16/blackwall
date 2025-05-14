function getCookieByName(name) {
     const cookies = document.cookie.split(';');
     for (let cookie of cookies) {
          cookie = cookie.trim();
          if (cookie.startsWith(name + '=')) {
             return cookie.substring(name.length + 1);
          }
     }
    return null;
}

async function send_to_server(endpoint, data) {
    await fetch(endpoint,
        {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json;charset=utf-8'
            },
            body: JSON.stringify(data)
        })
        .then(response => console.log(response, response.status))
        .catch(error => console.log(error, error.status))
}
async function ask_server(endpoint) {
    await fetch(endpoint)
    .then(response => {return response})
    .catch(error => console.log(error))
}