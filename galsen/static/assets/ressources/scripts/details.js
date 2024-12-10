// Details Products
document.addEventListener('DOMContentLoaded', function() {
    // Gestion des miniatures
    const mainImage = document.querySelector('.product-main-image');
    const thumbnails = document.querySelectorAll('.thumbnail');
    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', function() {
            // Mise à jour de l'image principale
            mainImage.src = this.src;
            
            // Mise à jour de la classe active
            thumbnails.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
        });
    });
    // Gestion de la quantité
    const minusBtn = document.querySelector('.quantity-btn.minus');
    const plusBtn = document.querySelector('.quantity-btn.max');
    const quantityInput = document.querySelector('.quantity-input');
    minusBtn.addEventListener('click', () => {
        const currentValue = parseInt(quantityInput.value);
        if (currentValue > 1) {
            quantityInput.value = currentValue - 1;
        }
    });
    plusBtn.addEventListener('click', () => {
        const currentValue = parseInt(quantityInput.value);
        quantityInput.value = currentValue + 1;
    });
    // Gestion du panier
    const addToCartBtn = document.querySelector('.add-to-cart-btn');
    addToCartBtn.addEventListener('click', () => {
        const quantity = parseInt(quantityInput.value);
        alert(`${quantity} produit(s) ajouté(s) au panier`);
    });
});