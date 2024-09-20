// ============== Bouton Links ==========
const freindlinks = document.querySelectorAll('.freinds');

// ===== Remove Bouton Links =====
const changeActiveLink = () => {
    freindlinks.forEach(link => {
        link.classList.remove('freind-active');
    })
}

freindlinks.forEach(link => {
    link.addEventListener('click', () => {
        changeActiveLink();
        link.classList.add('freind-active');
    })
})

// ========== Filters Tabs =====
// ========== Filters Tabs =====
const tabs = document.querySelectorAll('[data-target]'),
       tabContents = document.querySelectorAll('[data-content]')

tabs.forEach(tab =>{
    tab.addEventListener('click', () =>{
        const target = document.querySelector(tab.dataset.target)

        tabContents.forEach(tc =>{
            tc.classList.remove('filters__active')
        })
        target.classList.add('filters__active')

        tabs.forEach(t =>{
            t.classList.remove('filter-tab-active')
        })
        tab.classList.add('filter-tab-active')
    })
})
