
async function sendLoc(location){
    let myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    
    let raw = JSON.stringify(location);
    
    let requestOptions = {
      method: 'POST',
      headers: myHeaders,
      body: raw,
      redirect: 'follow'
    };
    
    fetch(`${BASE_URL}/location`, requestOptions)
      .then(response => response.text())
      .catch(error => console.log('error', error));
}

async function getCity(){
    let res = await axios.get(`${BASE_URL}/citysess`)
    let city = res.data['city']
    $('.set_location').replaceWith(` <p>Your location is currently set to ${city}</p>`)
}

