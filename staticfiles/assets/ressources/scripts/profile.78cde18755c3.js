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

// Change Background Header (Changement du Background)
function scrollHeader(){
  const header = document.getElementById('header')

  // When the scroll is greater than 80 viewport height, add the scroll-header class to the header class to the header tag
  if(this.scrollY >= 80) header.classList.add('scroll-header'); else header.classList.remove('scroll-header')
}
window.addEventListener('scroll', scrollHeader)

// ========== APEX CHART ==============
document.addEventListener("DOMContentLoaded", function() {
    var options = {
		series: [{
		name: 'series1',
		data: [31, 40, 28, 51, 42, 109, 100]
	  }, {
		name: 'series2',
		data: [11, 32, 45, 32, 34, 52, 41]
	  }],
		chart: {
		height: 350,
		type: 'area'
	  },
	  dataLabels: {
		enabled: false
	  },
	  stroke: {
		curve: 'smooth'
	  },
	  xaxis: {
		type: 'datetime',
		categories: ["2018-09-19T00:00:00.000Z", "2018-09-19T01:30:00.000Z", "2018-09-19T02:30:00.000Z", "2018-09-19T03:30:00.000Z", "2018-09-19T04:30:00.000Z", "2018-09-19T05:30:00.000Z", "2018-09-19T06:30:00.000Z"]
	  },
	  tooltip: {
		x: {
		  format: 'dd/MM/yy HH:mm'
		},
	  },
	  };
	  
	  var chart = new ApexCharts(document.querySelector("#chart"), options);
	  chart.render();
});

// ============= MENUS ==================
const allMenu = document.querySelectorAll('.content-data .head .menu');

allMenu.forEach(item => {
    const icon = item.querySelector('.icon');
    const menuLink = item.querySelector('.menu-link');

    icon.addEventListener('click', function () {
        menuLink.classList.toggle('show');
    })
})


window.addEventListener('click', function (e) {
    if(e.target !== imgProfile) {
        if(e.target !== dropdownProfile) {
            if(dropdownProfile.classList.contains('show')) {
                dropdownProfile.classList.remove('show');
            }
        }
    }

    allMenu.forEach(item => {
        const icon = item.querySelector('.icon');
        const menuLink = item.querySelector('.menu-link');
    
        if(e.target !== icon) {
            if(e.target !== menuLink) {
                if (menuLink.classList.contains ('show')) {
                    menuLink.classList.remove('show');
                }
            }
        }
    })

})