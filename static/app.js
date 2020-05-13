// const BASE_URL ='http://127.0.0.1:5000'
const BASE_URL = 'https://restaurant-roulette-v1.herokuapp.com/'

let savedRes = []
let clickedID = []
let username = []
let resInfo = {}
let userFav = []

//location function
async function init(){
    savedRes = []
    clickedID = []
    username = []
    resInfo = {}
    getUser()
   
  let lat = localStorage.getItem('lat')
  let lon = localStorage.getItem('lon')
    if(!lat && !lon){
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
}

$('#user_location').submit(async function(evt){
    evt.preventDefault()
    let city = $('#city').val()
    document.querySelector('#city').value=""
    $('#messages').removeClass('hide')
    $('#messages').append(`<small class="text-muted">Location Added!</small>`);
    let res = await axios.get(`${BASE_URL}/getloc/${city}`)
    let data = res['data']
    let lat = data['lat']
    let lon = data['lon']
    localStorage.removeItem('lat')
    localStorage.removeItem('lon')
    localStorage.setItem('lat', lat)
    localStorage.setItem('lon', lon)
    let location ={
        'lat': lat,
        'lon': lon
    }
    sendLoc(location)
})


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



async function getUser(){
    let user = await axios.get(`${BASE_URL}/checkuser`)
    if(user.data['Error']){
    }else{
        username.push(user.data['username'])
    }
}   

//Adding and removing favorites
async function getFav(){
    userFav = []
    let fav = await axios.get(`${BASE_URL}/getfav`)
    let jsonString = JSON.stringify(fav)
    let jsonResult = (JSON.parse(jsonString))
    for(res of jsonResult.data){
        userFav.push(res['name'])
    }
}


$('.resultsDiv').on('click',"#res-id", async function(evt){
    evt.preventDefault()
    await getFav()
    let name = $(this).attr('data-id')
    let checkFav = userFav.includes(name)
    if(checkFav){
        let res_id = $(this).attr('data-id')
        findID(res_id)
        $(this).toggleClass('far fas')
    }else{
        $(this).toggleClass('far fas')
        const res = await axios.get(`${BASE_URL}/user/add_fav/`)
    }
})



$('.results-section').on('click',"#res-id", async function(evt){
        evt.preventDefault()
        let clicked = $(this)
        if(clicked.hasClass('far')){
            $(this).toggleClass('far fas')
            const res = await axios.get(`${BASE_URL}/user/add_fav`)
        }else{
            let res_id = $(this).attr('data-id')
            findID(res_id)
            $(this).toggleClass('far fas')
        }
    })

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


$('.card').on('click',"#fav-id", async function(evt){
    evt.preventDefault()
    const $fav = evt.target.closest('a')
    const fav = evt.target.getAttribute('data-id')
    $(this).toggleClass('fas far')
    let remove = await axios.post(`${BASE_URL}/fav/delete/${fav}`)
   
})

async function removeFav(res_id){
    $(this).toggleClass('fas far')
    let remove = await axios.post(`${BASE_URL}/fav/delete/${res_id}`)
}

// Getting a list of nearby restaurants and rendering a picked restaurant
$('.buttons').on('click', '#getNearby', async function(evt){
    evt.preventDefault()
    let resp = await axios.get(`${BASE_URL}/nearbyRes`)
    for(let res of resp.data){
        let result = $(nearbyHTML(res))
        $('.results').append(result)
        savedRes.push({
            id: res.id,
            name: res.name,
            image_url: res.image_url,
            rating: res.rating,
            phone: res.phone,
            review_count: res.review_count,
            price: charToNum(res.price),
            url: res.url
        })
    }
    $('.btn-area').append('<div class="btn saveBtn">Done</div>')
    $('.title').hide()
    $('.roulette').hide()
    $('.buttons').hide()
    $('#user_location').hide()
    $('.nearbyRes').prepend('<h5 class="display-4 text-center nearTitle" style="font-size: 2.9vw;">Choose at least 2 restaurants</h2>')
})


$('.nearbyRes').on('click', '.nearCard', function(evt){
    evt.preventDefault()
    $(this).toggleClass('saved')
    let id = $(this).find('#res_id').attr('data-id')
    if(clickedID.includes(id)){
        clickedID.pop(id)
    }else{
        clickedID.push(id)
    }
})

function getRandomID(ID){
    if(ID.length >= 2){
        let ranInd = Math.ceil(Math.random() * ID.length-1)
        return ranInd
    }else{
        let alert = '<div class="alert alert-danger" role="alert">Choose at least 2 restaurants!</div>'
        return $('.nearbyRes').append(alert)
    }
}


$('.nearbyRes').on('click',".saveBtn", async function(evt){
    evt.preventDefault()
    let id = getRandomID(clickedID)
    let result = clickedID[id]
    let picked = savedRes.find(function(e){
        return e.id == result 
    })
    if(username.length > 0){

        await getFav()
    }
  
    let pickedRes = (picked['name'])
    let checkFav = userFav.includes(pickedRes)
    
    let htmlres = randomPicked(picked)
    $('.results-section').append(htmlres)
    await getUser()
    if(username.length == 0){
        $('#res-id').removeClass('far fa-heart') 
    }else if(checkFav){
        $('#res-id').toggleClass('far fas')
    }
    $('.btn').hide()
    $('.nearbyRes').hide()
    
    let data = JSON.stringify(picked)    
    sendRes(data)

})

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

// Render a single result wwhen wheel is clicked
$('.roulette').on('click', "#btn-spin", async function(evt){
    evt.preventDefault()
    $('.wheel').addClass('rotate')
    let resp = await axios.get(`${BASE_URL}/spin`)
    let result = resp.data
    resInfo ={
        'name': resp.data[0].name,
        'id': resp.data[0].id,
        'rating': resp.data[0].rating,
        'price': charToNum(resp.data[0].price),
        'image_url': resp.data[0].image_url,
        'phone': resp.data[0].phone,
        'review_count': resp.data[0].review_count,
        'url': resp.data[0].url
    }
    await getUser()
    if(username.length > 0){
        await getFav()
    }
 
    let checkFav = userFav.includes(resInfo['name'])
     
    setTimeout(() =>{
        $('.roulette').hide()
        $('.buttons').hide()
        $('.title').hide()
        $('#user_location').hide()
        $('#messages').hide()
        let htmlres = $(renderHTML(result))
        $('.results-section').append(htmlres)
        if(username.length == 0){
            $('#near-id').removeClass('far fa-heart') 
        }if(checkFav){
            $('#near-id').toggleClass('far fas')
        }
    }, 1000)
})

$('.results-section').on('click', '#near-id', async function(evt){
    evt.preventDefault()
    await getUser()
    await getFav()
    if($(this).hasClass('fas')){
        $('#near-id').toggleClass('fas far')
        findID(resInfo['name'])

    }else{
        let data = JSON.stringify(resInfo)
        sendRes(data)
        $(this).toggleClass('far fas')
        const res = await axios.get(`${BASE_URL}/user/add_fav`)
    }
})

//HTML functions 
function charToNum(char){
    if(char == '$'){
        return 1
    }else if(char == '$$'){
        return 2
    }else if(char == '$$$'){
        return 3
    }else if(char == '$$$$'){
        return 4
    }else{
        return 'n/a'
    }
}

function numToChar(num){
    if(num == 1){
        return "$"
    }else if(num == 2){
        return "$$"
    }else if(num == 3){
        return "$$$"
    }else if(num == 4){
        return "$$$$"
    }else{
        return 'n/a'
    }
}

function rating(resp){
    if(parseInt(resp) === resp){
        let img=` <img src="/static/images/yelp_stars/web_and_ios/small/small_${resp}.png" alt=""> `
        return img
    }else{
        let int = Math.trunc(resp)
        let img=` <img src="/static/images/yelp_stars/web_and_ios/small/small_${int}_half.png" alt=""> `
        return img
    }
}
   
function nearbyHTML(resp){
    let res = resp.rating
    let star = rating(res)
    return `
    <div class="col-lg-3 col-md-4 d-flex align-items-stretch">
    <div class="card nearCard shadow mt-3" style="width: 18rem;">
        <img src="${resp.image_url}" id="res_id" data-id="${resp.id}" class="card-img-top" alt="..." data-img="${resp.image_url}">
        <div class="card-img-overlay d-flex flex-row justify-content-end">
          <i id="near-id" data-id=${resp.name}class="fas fa-plus" style="color:white; font-size: 2em; text-decoration: none;" ></i>
      </div>
        <div class="card-body">
        <h5 class="card-title" id="name" data-name=${resp.name}>${resp.name}</h5>
        <p class="card-text" id='res' data-res=${res}>${res} ${star}</p>
        <p class="card-text" id="rev" data-revcount=${resp.review_count} >${resp.review_count} reviews </p>
        <p class="card-text" id="price" data-price=${resp.price} >${resp.price || 'n/a'}</p>
      </div>
    </div>
    </div>
    
    `
}
   
function randomPicked(resp){
    let res = resp.rating
    let star = rating(res)
    let price = numToChar(resp.price)
    return `
    <div class="card shadow mt-3" style="width: 18rem;">
        <img src="${resp.image_url}" id="res_id" data-id="${resp.id}" class="card-img-top" alt="..." data-img="${resp.image_url}">
        <div class="card-img-overlay d-flex flex-row justify-content-end">
          <i id="res-id" data-resid="${resp.id}"data-id="${resp.name}"class="far fa-heart" style="color:white; font-size: 2em; text-decoration: none;" ></i>
      </div>
        <div class="card-body">
        <h5 class="card-title" id="name" data-name=${resp.name}>${resp.name}</h5>
        <p class="card-text" id='res' data-res=${res}>${res} ${star}</p>
        <p class="card-text" id="rev" data-revcount=${resp.review_count} >${resp.review_count} reviews </p>
        <p class="card-text" id="price" data-price=${resp.price} >${price || 'n/a'}</p>
        <i class="fa fa-yelp" style="color:red" aria-hidden="true"></i>
        <a href="${resp.url}" class="card-link text-danger">More Info</a>
        <p class="card-text"><small class="text">Powered by Yelp</small></p>
      </div>
      </div>
    `
}

function renderHTML(resp){
    let res = resp[0].rating
    let star = rating(res)
    return `
    <div class="row">
    <div class="col">
    <div class="card shadow" style="width: 18rem;">
        <img src="${resp[0].image_url}" class="card-img-top" alt="...">
        <div class="card-img-overlay d-flex flex-row justify-content-end">
        <a href="" data-id="${resp[0].name}" id="near-id" class="far fa-heart" style="color:white; font-size: 2em; text-decoration: none;" ></a>
        </div>
        <div class="card-body">
        <h5 class="card-title">${resp[0].name}</h5>
        <p class="card-text">${res} ${star}</p>
        <p class="card-text">${resp[0].review_count} reviews </p>
        <p class="card-text">
        <svg class="bi bi-phone" width="1em" height="1em" viewBox="0 0 16 16" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
            <path fill-rule="evenodd" d="M11 1H5a1 1 0 00-1 1v12a1 1 0 001 1h6a1 1 0 001-1V2a1 1 0 00-1-1zM5 0a2 2 0 00-2 2v12a2 2 0 002 2h6a2 2 0 002-2V2a2 2 0 00-2-2H5z" clip-rule="evenodd"/>
            <path fill-rule="evenodd" d="M8 14a1 1 0 100-2 1 1 0 000 2z" clip-rule="evenodd"/>
          </svg>${resp[0].phone}</p>
        <p class="card-text">${resp[0].price || 'n/a'}</p>
        <i class="fa fa-yelp" style="color:red" aria-hidden="true"></i>
        <a href="${resp[0].url}" class="card-link text-danger">More Info</a><br>
        <p class="card-text"><small class="text">Powered by Yelp</small></p>
      </div>
    </div>
    <div class="row">
    <div class="col my-3 d-flex justify-content-center">
    <a href="/" class="btn shadow">Home Page</a>
    </div>
`
}


init()





