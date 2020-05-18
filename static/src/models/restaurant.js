
async function getFav(){
    userFav = []
    let fav = await axios.get(`${BASE_URL}/getfav`)
    let jsonString = JSON.stringify(fav)
    let jsonResult = (JSON.parse(jsonString))
    for(res of jsonResult.data){
        userFav.push(res['name'])
    }
  }

async function findID(res){
    let myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    
    let raw = JSON.stringify(res);
    
    let requestOptions = {
      method: 'POST',
      headers: myHeaders,
      body: raw,
      redirect: 'follow'
    };
    
    fetch(`${BASE_URL}/findID`, requestOptions)
      .then(response => response.text())
      .catch(error => console.log('error', error));
}

async function removeFav(res_id){
    $(this).toggleClass('fas far')
    let remove = await axios.post(`${BASE_URL}/fav/delete/${res_id}`)
}

async function sendRes(res){
    let myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");
    
    let raw = JSON.stringify(res);
    
    let requestOptions = {
      method: 'POST',
      headers: myHeaders,
      body: raw,
      redirect: 'follow'
    };
    
    fetch(`${BASE_URL}/handleRes`, requestOptions)
      .then(response => response.text())
      .catch(error => console.log('error', error));
}