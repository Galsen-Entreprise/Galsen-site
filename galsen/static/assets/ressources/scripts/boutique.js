// slider
var boutique = 0;
var P = 0;
var sliderBoutique = document.getElementsByClassName("slider-boutique");
var lineBoutique = document.getElementsByClassName("line-boutique");

autoBoutique();

function showBoutique(n) {
    for(P = 0; P < sliderBoutique.length; P++) {
        sliderBoutique[P].style.display = "none";
    }
    for(P = 0; P < lineBoutique.length; P++) {
        lineBoutique[P].className = lineBoutique[P].className.replace("activeBoutique");
    }
    sliderBoutique[n - 1].style.display = ("block");
    lineBoutique[n - 1].className += " activeBoutique";
}

function autoBoutique() {
    boutique ++;
    if (boutique > sliderBoutique.length) {
        boutique = 1;
    }
    showBoutique(boutique);
    setTimeout(autoBoutique, 5000);
}

function plusSlideBoutique(n) {
    boutique+=n;
    if (boutique > sliderBoutique.length) {
        boutique=1;
    }
    if(boutique < 1) {
        boutique=sliderBoutique.length;
    }
    showBoutique(boutique);
}

function currentSlideBoutique(n) {
    boutique = n;
    showBoutique(boutique);
}
// End