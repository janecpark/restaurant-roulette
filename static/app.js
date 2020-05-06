const BASE_URL ='http://127.0.0.1:5000'
// const BASE_URL = "http://localhost:5000/api";



// $('#fav-save').on('click', async function(evt){
//     // debugger;
//     evt.preventDefault()
//     console.log(evt.target)
//     const rest_id = evt.target.getAttribute('data-id')
//     const res = await axios.post(`${BASE_URL}/user/add_fav/${rest_id}`, {rest_id})


// })


$('.card').on('click',"#fav-id", async function(evt){
    evt.preventDefault()
    const $fav = $(evt.target).parent().parent()
    const fav = evt.target.getAttribute('data-id')
    console.log($fav)
    if($("#fav-id").hasClass('fas')){
        await axios.delete(`${BASE_URL}/fav/delete/${fav}`)
        $fav.remove();
    }
})