// Caption Image
let uploadimg = document.getElementById("upload-button");
let choosenimg = document.getElementById("choosen-image");


uploadimg.onchange = () => {
    let reader = new FileReader();
    reader.readAsDataURL(uploadimg.files[0]);
    reader.onload = () => {
        choosenimg.setAttribute("src", reader.result);
    } 

    fileNameimg.textContent = uploadimg.files[0].name;
}

// Caption Video
let uploadVideo = document.getElementById("upload-button_Video");
let choosenVideo = document.getElementById("choosen-video");


uploadVideo.onchange = () => {
    let reader = new FileReader();
    reader.readAsDataURL(uploadVideo.files[0]);
    reader.onload = () => {
        choosenVideo.setAttribute("src", reader.result);
    } 

    fileNameVideo.textContent = uploadVideo.files[0].name;
}