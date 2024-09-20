const viewBtn = document.querySelector("#pop-share"),
    popup = document.querySelector(".popup-share"),
    close = popup.querySelector(".close");
    // field = popup.querySelector(".field"),
    // input = field.querySelector("input"),
    // copy = field.querySelector(".cop");

    document.querySelectorAll('.center #pop-share').forEach(viewBtn => {
        viewBtn.onclick = ()=>{
            popup.classList.toggle("show");
          }
          close.onclick = ()=>{
            viewBtn.click();
          }
    })

    // copy.onclick = ()=>{
    //   input.select(); //select input value
    //   if(document.execCommand("copy")){ //if the selected text copy
    //     field.classList.add("active");
    //     copy.innerText = "Copié";
    //     setTimeout(()=>{
    //       window.getSelection().removeAllRanges(); //remove selection from document
    //       field.classList.remove("active");
    //       copy.innerText = "Copy";
    //     }, 3000);
    //   }
    // }

    
// Show Popup
let pol = document.querySelectorAll('.center .content_offert');

pol.forEach(vid => 
{
vid.onclick = () =>
{

    pol.forEach(remove => {remove.classList.remove('activ')});
    vid.classList.add('activ');
    
    let share = vid.querySelector('.contenu').innerHTML;

    
    document.querySelector('.popup-share .content').innerHTML = share;
}
})