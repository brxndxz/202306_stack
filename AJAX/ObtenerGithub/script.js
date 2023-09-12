var boton = document.querySelector("button").addEventListener("click", getGitUser);

async function getGitUser(){
    var response = await fetch("https://api.github.com/users/adion81");
    var data = await response.json();
    console.log(data);
    return data;
    
}

var info = document.getElementById("show-info");
var image = document.getElementById("show-image");

async function show(data){
    console.log("data")
    info.innerHTML = data.name + "has" + data.followers + "followers";
}
