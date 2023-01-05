
var mykey = config.API_KEY;
fetch("https://youtube.googleapis.com/youtube/v3/search?part=snippet&channelId=UCj0V0aG4LcdHmdPJ7aTtSCQ&maxResults=8&order=date&key="+mykey)
.then((result)=>{
    return result.json()

}).then((data)=>{
    console.log(data)
    let videos = data.items
    let video = document.querySelector(".videos")
    for (e of videos){
        video.innerHTML += `
            
               <iframe class="mr-3" id="player" width="180" height="100" 
                   src="https://www.youtube.com/embed/${e.id.videoId}">
               </iframe>
               <div>
               <h6 class="">${e.snippet.title}</h6>
               </div>
            
                
        `
    }
})


