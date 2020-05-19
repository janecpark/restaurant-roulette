
$('.card').on('click',"#fav-id", async function(evt){
    evt.preventDefault()
    const $fav = evt.target.closest('a')
    const fav = evt.target.getAttribute('data-id')
    $(this).toggleClass('fas far')
    await axios.post(`${BASE_URL}/fav/delete/${fav}`)
   
})

$('.resultsDiv').on('click',".res-id", async function(evt){
    evt.preventDefault()
    let res_id = $(this).attr('data-id')
    if($(this).hasClass('addfav')){
        $(this).toggleClass('addfav removefav')
        $(this).text('Remove Favorite')
        await axios.get(`${BASE_URL}/add_fav/`)
        
    }else{
        $(this).text('Add Favorite')
        $(this).toggleClass('removefav addfav')
        findID(res_id)
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
            price: res.price,
            url: res.url,
            address: res.location['address1'],
            city: res.location['city'],
            state: res.location['state'],
            zip_code: res.location['zip_code'],

        })
    }
    $('.btn-area').append('<div class="btn saveBtn mb-5">Done</div>')
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
    sendRes(picked)
})

function hidePage(){
    $('.buttons').hide()
    $('.quick-search').hide()
    $('.content-banner').hide()
    $('#user_location').hide()
    $('.title').hide()
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
   
