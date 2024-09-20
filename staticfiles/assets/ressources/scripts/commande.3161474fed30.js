const button = document.querySelector(".Learn");

button.addEventListener("click", (e) => {
    e.preventDefault();
    button.classList.add("animate");

    setTimeout(() => {
        button.classList.remove("animate");
    }, 600)
});


// Change Image on click
function imgSlider(anything) {
    document.querySelector('.fruits').src = anything
}

// Active Select
let el =document.querySelectorAll('.thumb li');
for (let i = 0; i < el.length; i++) {
    el[i].onclick = function() {
        var c = 0;
        while (c < el.length) {
            el[c++].className = 'check';
        }
        el[i].className = 'check active';
    }
}


// Popup Commande
document.addEventListener("DOMContentLoaded", function() {
    const commandeButton = document.getElementById("Commande");
    const popup = document.getElementById("valide-commande");
    const closePopup = document.getElementById("close_views");
  
    commandeButton.addEventListener("click", function() {
      popup.style.display = "block";
    });
  
    closePopup.addEventListener("click", function() {
      popup.style.display = "none";
    });
  
    window.addEventListener("click", function(event) {
      if (event.target == popup) {
        popup.style.display = "none";
      }
    });
  });