
$('.full-result').on('click', '#res-id', async function(evt){
    evt.preventDefault()
       await getFav();
       let name = $(this).attr('data-id')
       let checkFav = userFav.includes(name);
       if(checkFav){
           let res_id = $(this).attr('data-id');
           findID(res_id);
           $(this).toggleClass('far fas');
       }else{
           $(this).toggleClass('far fas');
           const res = await axios.get(`${BASE_URL}/add_fav/`);
       }
   })

   $('.card').on('click',"#fav-id", async function(evt){
    evt.preventDefault()
    const $fav = evt.target.closest('a')
    const fav = evt.target.getAttribute('data-id')
    $(this).toggleClass('fas far')
    let remove = await axios.post(`${BASE_URL}/fav/delete/${fav}`)
   
})

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
        const res = await axios.get(`${BASE_URL}/add_fav/`)
    }
})

   
   $('.results-section').on('click', '#res-id', async function(evt){
          evt.preventDefault()
       let clicked = $(this)
       if(clicked.hasClass('far')){
           $(this).toggleClass('far fas')
           const res = await axios.get(`${BASE_URL}/add_fav`)
       }else{
           let res_id = $(this).attr('data-id')
           findID(res_id)
           $(this).toggleClass('far fas')
       }
   })
   


$('.buttons').one('click', '#getNearby', async function(evt){
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
            url: res.url,
            address: res.location['address1'],
            city: res.location['city'],
            state: res.location['state'],
            zip_code: res.location['zip_code'],

        })
    }
    $('.btn-area').append('<div class="btn saveBtn">Done</div>')
    hidePage()
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

$('.nearbyRes').one('click',".saveBtn", async function(evt){
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
    let htmlres = fullInfo(picked)
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

async function getRestaurant(type){
        let response = await axios.get(`${BASE_URL}/cuisine/${type}`)
        let result = response.data[0]
        if(result.length == 0){
            let alert = '<div class="alert alert-danger" role="alert">No result!</div>'
            return $('.quick-search').prepend(alert)
        }
        resInfo ={
            'name': result.name
        }

        await getUser()
        if(username.length > 0){
        await getFav()
    }
   
    let checkFav = userFav.includes(resInfo['name'])
    hidePage()
    let htmlres = $(fullInfo(result))
    $('.full-result').append(htmlres)
    if(username.length == 0){
        $('#near-id').removeClass('far fa-heart') 
    }if(checkFav){
        $('#near-id').toggleClass('far fas')
    }
  }

 

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
        const res = await axios.get(`${BASE_URL}/add_fav`)
    }
})

function hidePage(){
    $('.buttons').hide()
    $('.quick-search').hide()
    $('.content-banner').hide()
    $('#user_location').hide()
    $('.title').hide()

  }

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
    if(!Number.isInteger(num)){
        return 
    }
    else if(num == 1){
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

function rating(resp, size){
    if(parseInt(resp) === resp){
        let img=` <img src="/static/images/yelp_stars/web_and_ios/${size}/${size}_${resp}.png" alt=""> `
        return img
    }else{
        let int = Math.trunc(resp)
        let img=` <img src="/static/images/yelp_stars/web_and_ios/${size}/${size}_${int}_half.png" alt=""> `
        return img
    }
}
   
function nearbyHTML(resp){
    let res = resp.rating
    let star = rating(res, 'small')
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
   

function fullInfo(resp){
    let res = resp.rating
    let star = rating(res, 'large')
    let price = numToChar(resp.price)
    return `
    <div class="card shadow mt-3 mb-5 " style="width: 40rem;">
    <img src="${resp.image_url}" id="res_id" data-id="${resp.id}" class="card-img-top img-fluid" alt="..." data-img="${resp.image_url}">
    <div class="card-img-overlay d-flex flex-row justify-content-end">
      <i id="res-id" data-resid="${resp.id}"data-id="${resp.name}"class="far fa-heart" style="color:white; font-size: 2em; text-decoration: none;" ></i>
  </div>
    <div class="card-body">
    <h5 class="card-title" id="name" data-name=${resp.name}>${resp.name}</h5>
    <p class="card-text" id='res' data-res=${res}>${res} ${star}</p>
    <p class="card-text" id="rev" data-revcount=${resp.review_count} >${resp.review_count} reviews </p>
    <p class="card-text" id="price" data-price=${resp.price}>${price || resp.price || 'n/a'}</p>
    <p class="card-text"> ${resp.address || resp.location['address1']} 
    ${resp.city || resp.location['city']} ${resp.state || resp.location['state']}, ${resp.zip_code || resp.location['zip_code']}</p>
    <i class="fa fa-yelp" style="color:red" aria-hidden="true"></i>
    <a href="${resp.url}" class="card-link text-danger">More Info</a>
    <p class="card-text"><small class="text">Powered by Yelp</small></p>
  </div>
  </div>
  
`   
}
