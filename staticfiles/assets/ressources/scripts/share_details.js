document.addEventListener("DOMContentLoaded", function() {
    const shareButton = document.getElementById("shareButton");
    const popup = document.getElementById("popup");
    const closePopup = document.getElementById("closePopup");
  
    shareButton.addEventListener("click", function() {
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
  