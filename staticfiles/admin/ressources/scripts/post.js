// Description
const voirPlus = document.getElementsByClassName('content-post');

    for (i = 0; i<voirPlus.length; i++) {
        voirPlus[i].addEventListener('click', function(){
            this.classList.toggle('actipe');
        })
    }