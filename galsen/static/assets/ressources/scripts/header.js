// Change Background Header (Changement du Background)
function scrollHeader(){
    const header = document.getElementById('header')

    // When the scroll is greater than 80 viewport height, add the scroll-header class to the header class to the header tag
    if(this.scrollY >= 80) header.classList.add('scroll-header'); else header.classList.remove('scroll-header')
}
window.addEventListener('scroll', scrollHeader)


// ============== Bouton Links ==========
const navlinks = document.querySelectorAll('.nav_link');

// ===== Remove Bouton Links =====
// const changeActiveLink = () => {
//     navlinks.forEach(link => {
//         link.classList.remove('active-link');
//     })
// }

navlinks.forEach(link => {
    link.addEventListener('click', () => {
        changeActiveLink();
        link.classList.add('active-link');
    })
})

const showMenu = (headerToggle, nabbarId) => {
    const toggleBtn = document.getElementById(headerToggle),
      nab = document.getElementById(nabbarId)
 
    if (headerToggle &&  nabbarId) {
      toggleBtn.addEventListener('click', () => {
        nab.classList.toggle('show-menu')
        toggleBtn.classList.toggle('fa-times')
      })
    }
  }

  showMenu('header-toggle', 'nabbar')

 const linkcolor = document.querySelectorAll('.nab_link');

 function colorLink() {
   linkcolor.forEach(l => l.classList.remove('active'))
   this.classList.add('active')
 }
 linkcolor.forEach(l => l.addEventListener('click', colorLink))

// button Menu
const butn = document.querySelectorAll('.conta_menu');

for(let i = 0; i < butn.length; i++ ) {
    butn[i].addEventListener('click', function(e) {
        butn[i].classList.toggle('button-cliked');
        butn[i].firstElementChild.classList.toggle('icon-cliked');
    }) 
}

