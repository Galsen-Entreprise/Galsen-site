// SidebarRight Politique
var sidebarPolitic = 0;
var RP = 0;
var sliderRP = document.getElementsByClassName("sliderRP");
var lineRP = document.getElementsByClassName("line_RP");

autoRP();

function showRP(n) {
    for(RP = 0; RP < sliderRP.length; RP++) {
        sliderRP[RP].style.display = "none";
    }
    for(RP = 0; RP < lineRP.length; RP++) {
        lineRP[RP].className = lineRP[RP].className.replace("activehP");
    }
    sliderRP[n - 1].style.display = ("block");
    lineRP[n - 1].className += " activehP";
}

function autoRP() {
    sidebarPolitic ++;
    if (sidebarPolitic > sliderRP.length) {
        sidebarPolitic = 1;
    }
    showRP(sidebarPolitic);
    setTimeout(autoRP, 5000);
}

function plusSlideRP(n) {
    sidebarPolitic+=n;
    if (sidebarPolitic > sliderRP.length) {
        sidebarPolitic=1;
    }
    if(sidebarPolitic < 1) {
        sidebarPolitic=sliderRP.length;
    }
    showRP(sidebarPolitic);
}

function currentSlideRP(n) {
    sidebarPolitic = n;
    showRP(sidebarPolitic);
}
// End