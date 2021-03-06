$(document).ready(function(){
    const card = $('.card');
    const results = $('.resultsDiv');
    const buttons = $('.buttons');
    const nearResult = $('.nearbyRes');
    const redo = $('.redo-search');

    /* Add loading spinner */

    let $loading = $('.spinner-border').hide()
    $(document)
        .ajaxStart(function(){
            $loading.show();
    })
        .ajaxStop(function(){
            $loading.hide();
    })

    /* Toggle favorites on restaurant cards  */

    card.on('click',"#fav-id", async function(evt){
        evt.preventDefault()
        const $fav = evt.target.closest('a')
        const fav = evt.target.getAttribute('data-id')
        $(this).toggleClass('fas far')
        removeName(fav)
    })

    /* Toggle favorites on results page  */

    results.on('click',".res-id", async function(evt){
        evt.preventDefault()
        let res_id = $(this).attr('data-id')
        if($(this).hasClass('addfav')){
            $(this).toggleClass('addfav removefav')
            $(this).text('Remove Favorite')
            addFav()
            
        }else{
            $(this).text('Add Favorite')
            $(this).toggleClass('removefav addfav')
            findID(res_id)
        }
    })

    /* Redo search on results page   */

    redo.on("click", async function(evt){
        evt.preventDefault();
        const type = evt.target.getAttribute('data-type')
        getRestaurant(type)
    })

    /* Show a list of nearby restaurants for users to choose from   */

    buttons.one('click', '#getNearby', async function(evt){
        evt.preventDefault()
        
            $.ajax(`${BASE_URL}/nearbyRes`, {
        success: response => {
                for(let res of response){
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
                    type: res.categories[0]['alias']
                })
            }
            $('.btn-area').append('<div class="btn saveBtn mb-5">Done</div>')
            hidePage()
            $('.nearbyRes').prepend('<h5 class="display-4 text-center nearTitle" style="font-size: 2.9vw;">Choose at least 2 restaurants</h2>')
        },
            error: error => {
            window.location.href = `${BASE_URL}/error`;
        }
        })
    })

    /* Let users click on the cards to add/remove to list  */

    nearResult.on('click', '.nearCard', function(evt){
        evt.preventDefault()
        $(this).toggleClass('saved')
        let id = $(this).find('#res_id').attr('data-id')
        if(clickedID.includes(id)){
            clickedID.pop(id)
        }else{
            clickedID.push(id)
        }
    })

    /* Get random restaurant and send to server  */

    nearResult.one('click',".saveBtn", async function(evt){
        evt.preventDefault()
        let id = getRandomID(clickedID)
        let result = clickedID[id]
        let picked = savedRes.find(function(e){
            return e.id == result 
        })
        sendRes(picked)
    })

    /* Choose a random restaurant from user's list */

    function getRandomID(ID){
        if(ID.length >= 2){
            let ranInd = Math.ceil(Math.random() * ID.length-1)
            return ranInd
        }else{
            let alert = '<div class="alert alert-danger" role="alert">Choose at least 2 restaurants!</div>'
            return $('.nearbyRes').append(alert)
        }
    }

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

    /* Render HTML for nearby restaurant  */
    
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
            <p class="card-text" id="rev" data-revcount=${resp.review_count}>${resp.review_count} reviews </p>
            <p class="card-text" id="price" data-price=${resp.price} >${resp.price || 'n/a'}</p>
        </div>
        </div>
        </div>
        `
    }
   
})