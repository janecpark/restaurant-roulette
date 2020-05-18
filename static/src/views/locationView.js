
$('#user_location').submit(async function(evt){
    evt.preventDefault()
    let city = $('#city').val()
    if (city === "") {
        $('.set_location').append("<div class='alert alert-danger'>Please enter city or zipcode.</div>");
    return false;
    }
    document.querySelector('#city').value=""
    let res = await axios.get(`${BASE_URL}/getloc/${city}`)
    let data = res['data']
    let lat = data['lat']
    let lon = data['lon']
    localStorage.removeItem('lat')
    localStorage.removeItem('lon')
    localStorage.setItem('lat', lat)
    localStorage.setItem('lon', lon)
    getCity()
})


