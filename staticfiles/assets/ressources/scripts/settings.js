const params = document.querySelectorAll(".param");

params.forEach(param => {
    param.addEventListener("click", () => {
        params.forEach(item => {
            if (item !== param) {
                item.classList.remove("active");
            }
        })
        param.classList.toggle("active");
    })
})