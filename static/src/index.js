const BASE_URL ='http://127.0.0.1:5000'
// const BASE_URL = 'https://restaurant-roulette-v1.herokuapp.com'
let savedRes = []
let clickedID = []
let resInfo = {}
let userFav = []

async function init(){
    savedRes = []
    clickedID = []
    username = []
    resInfo = {}
    serverSess()
    
  let lat = localStorage.getItem('lat')
  let lon = localStorage.getItem('lon')
  
    if(!lat && !lon){
      geoLocation()
    }  
}


function geoLocation(){
    navigator.geolocation.getCurrentPosition(function(position){
        let lat = position.coords.latitude;
        let lon = position.coords.longitude
        let location ={
            'lat': lat,
            'lon': lon
        }
        localStorage.setItem('lat', lat)
        localStorage.setItem('lon', lon)
        sendLoc(location)
    })
}

async function serverSess(){
    let resp = await axios.get(`${BASE_URL}/checksess`)
    if(resp.data['error']){
        geoLocation()
    }
}


init()


