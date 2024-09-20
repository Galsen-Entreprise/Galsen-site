const viewBtn = document.querySelector("#pop-share"),
    popup = document.querySelector(".popup-share"),
    close = popup.querySelector(".close"),
    field = popup.querySelector(".field"),
    input = field.querySelector("input"),
    copy = field.querySelector("button");

    document.querySelectorAll('.center #pop-share').forEach(viewBtn => {
        viewBtn.onclick = ()=>{
            popup.classList.toggle("show");
          }
          close.onclick = ()=>{
            viewBtn.click();
          }
    })

    copy.onclick = ()=>{
      input.select(); //select input value
      if(document.execCommand("copy")){ //if the selected text copy
        field.classList.add("active");
        copy.innerText = "Copié";
        setTimeout(()=>{
          window.getSelection().removeAllRanges(); //remove selection from document
          field.classList.remove("active");
          copy.innerText = "Copy";
        }, 3000);
      }
    }

// Show Popup
let politiList = document.querySelectorAll('.cadre-grid .cadre');

politiList.forEach(vid => 
{
vid.onclick = () =>
{

    politiList.forEach(remove => {remove.classList.remove('active')});
    vid.classList.add('active');
    
    let share = vid.querySelector('.contenu').innerHTML;

    
    document.querySelector('.popup-share .content').innerHTML = share;
}
})

// Select All Button
const btn = document.querySelectorAll('.like_btn');

let clicked = false;

// Add click Event for all button
for(let i = 0; i < btn.length; i++) {
    btn[i].addEventListener('click', function(e) {
        // add styles for the clicked Button
        btn[i].classList.toggle('button-cliked');

        btn[i].firstElementChild.classList.toggle
        ('icon-clicked');
    })
}
  

// 
const abn =document.querySelectorAll('.abonne_btn');


// Add click Event for all button
for(let i = 0; i < abn.length; i++) {
    abn[i].addEventListener('click', function(e) {
        // add styles for the clicked Button
        abn[i].classList.toggle('abonne-cliked');
        
        abn[i].firstElementChild.classList.toggle('text-clicked');
    })
}

// Show View Thop Affiche
const viewShowBtn = document.querySelector(".affiche"),
popupShow = document.querySelector(".popup-view-show"),
closup = popupShow.querySelector(".close");

document.querySelectorAll('.center .affiche').forEach(viewShowBtn => {
    viewShowBtn.onclick = ()=>{
        popupShow.classList.toggle("show-view");
    }
    closup.onclick = ()=>{
        viewShowBtn.click();
    }
})

let ShowView = document.querySelectorAll('.cadre-grid .cadre');

ShowView.forEach(vid => 
{
vid.onclick = () =>
{

  ShowView.forEach(remove => {remove.classList.remove('active')});
    vid.classList.add('active');
    
    let showview = vid.querySelector('.affiche').src;

    
    document.querySelector('.popup-view-show .view-show').src = showview;
}
})

// Popup Cv
const viewProposBtn = document.querySelector(".Profilage"),
popupPropos = document.querySelector(".popup-view-propos"),
closupPropos = popupPropos.querySelector(".close");

document.querySelectorAll('.center .Profilage').forEach(viewProposBtn => {
	viewProposBtn.onclick = ()=>{
		popupPropos.classList.toggle("show-propos");
	}
	closupPropos.onclick = ()=>{
		viewProposBtn.click();
	}
  })