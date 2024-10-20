// slider
var politic = 0;
var P = 0;
var sliderP = document.getElementsByClassName("sliderP");
var lineP = document.getElementsByClassName("line_P");

autoP();

function showP(n) {
    for(P = 0; P < sliderP.length; P++) {
        sliderP[P].style.display = "none";
    }
    for(P = 0; P < lineP.length; P++) {
        lineP[P].className = lineP[P].className.replace("activeP");
    }
    sliderP[n - 1].style.display = ("block");
    lineP[n - 1].className += " activeP";
}

function autoP() {
    politic ++;
    if (politic > sliderP.length) {
        politic = 1;
    }
    showP(politic);
    setTimeout(autoP, 5000);
}

function plusSlideP(n) {
    politic+=n;
    if (politic > sliderP.length) {
        politic=1;
    }
    if(politic < 1) {
        politic=sliderP.length;
    }
    showP(politic);
}

function currentSlideP(n) {
    politic = n;
    showP(politic);
}
// End