// Image Carroussel
document.addEventListener('DOMContentLoaded', () => {
    const mediaCarousels = document.querySelectorAll('.media-carousel');
    mediaCarousels.forEach(carousel => {
        const mediaWrapper = carousel.querySelector('.media-wrapper');
        const prevButton = carousel.querySelector('.prev-btn');
        const nextButton = carousel.querySelector('.next-btn');
        const closeButton = document.querySelector('.close_views');

        prevButton.addEventListener('click', () => scrollMedia('prev'));
        nextButton.addEventListener('click', () => scrollMedia('next'));
        mediaWrapper.addEventListener('click', openModal);
        closeButton.addEventListener('click', closeModal);


        let currentMedia = 0;
        let isDragging = false;
        let startPos = 0;
        let currentTranslate = 0;
        let prevTranslate = 0;
        let animationID;
        const mediaCount = mediaWrapper.children.length;
        
        function updateMediaIndicator() {
            const indicator = carousel.querySelector('.media-indicator');
            indicator.textContent = `${currentMedia + 1} / ${mediaCount}`;
        }
        
        function startDrag(event) {
            isDragging = true;
            startPos = getPositionX(event);
            animationID = requestAnimationFrame(animation);
            mediaWrapper.style.cursor = 'grabbing';
        }
        
        function onDrag(event) {
            if (isDragging) {
                const currentPosition = getPositionX(event);
                currentTranslate = prevTranslate + currentPosition - startPos;
            }
        }
        
        function endDrag() {
            isDragging = false;
            cancelAnimationFrame(animationID);
            const movedBy = currentTranslate - prevTranslate;
            if (movedBy < -100 && currentMedia < mediaCount - 1) {
                currentMedia += 1;
            }
            if (movedBy > 100 && currentMedia > 0) {
                currentMedia -= 1;
            }
            setPositionByIndex();
            updateMediaIndicator();
            mediaWrapper.style.cursor = 'grab';
        }
        
        function getPositionX(event) {
            return event.type.includes('mouse') ? event.pageX : event.touches[0].clientX;
        }
        
        function animation() {
            mediaWrapper.style.transform = `translateX(${currentTranslate}px)`;
            if (isDragging) requestAnimationFrame(animation);
        }
        
        function setPositionByIndex() {
            currentTranslate = currentMedia * -mediaWrapper.clientWidth;
            prevTranslate = currentTranslate;
            mediaWrapper.style.transform = `translateX(${currentTranslate}px)`;
        }

        function openModal(event) {
            // Vérifiez si l'élément cliqué est une image
            if (event.target.tagName === 'IMG') {
                const modal = document.getElementById('modal');
                const modalImg = document.getElementById('modal-img');
                const downloadLink = document.getElementById('download-link');
                
                // Affichez le modal
                modal.style.display = 'flex';
                
                // Définissez la source de l'image dans le modal
                modalImg.src = event.target.src;
                
                // Définissez le nom de fichier pour le lien de téléchargement
                const imageUrl = event.target.src;
                const imageName = imageUrl.substring(imageUrl.lastIndexOf('/') + 1);
                downloadLink.href = imageUrl;
                downloadLink.download = imageName;
            }
        }
        
        function closeModal() {
            const modal = document.getElementById('modal');
            modal.style.display = 'none';
        }
        
        function getFileNameFromURL(url) {
            return url.substring(url.lastIndexOf('/') + 1);
        }
        
        

        function scrollMedia(direction) {
            if (direction === 'next' && currentMedia < mediaCount - 1) {
                currentMedia += 1;
            } else if (direction === 'prev' && currentMedia > 0) {
                currentMedia -= 1;
            }
            setPositionByIndex();
            updateMediaIndicator();
        }

        carousel.addEventListener('touchstart', startDrag);
        carousel.addEventListener('touchmove', onDrag);
        carousel.addEventListener('touchend', endDrag);
        carousel.addEventListener('mousedown', startDrag);
        carousel.addEventListener('mousemove', onDrag);
        carousel.addEventListener('mouseup', endDrag);
        carousel.addEventListener('mouseleave', endDrag);
        
        updateMediaIndicator();

        
    });
});

// Like
$(document).ready(function() {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    $('.button-like').click(function(event) {
        event.preventDefault();
        
        var postId = $(this).data('post-id');
        var formData = $('#like-form-' + postId).serialize();
        
        $.ajax({
            url: $('#like-form-' + postId).attr('action'),
            method: 'POST',
            data: formData,
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            },
            success: function(data) {
                $('#likeIcon' + postId).html(data.like_icon);
                $('#likeIcon' + postId).next('.number-like').html(data.like_count);
            },
            error: function(xhr, status, error) {
                console.log('Error: ' + error);
            }
        });
    });
});

// Suivi
$(document).ready(function() {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    $('.subscribe-form').on('submit', function(event) {
        event.preventDefault();  // Empêche le rafraîchissement de la page

        var form = $(this);
        var userId = form.find('.button-follow').data('user-id');
        var formData = form.serialize();

        $.ajax({
            url: form.attr('action'),
            method: 'POST',
            data: formData,
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
                xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            },
            success: function(data) {
                // Mettre à jour le bouton en fonction de la réponse du serveur
                var button = form.find('.button-follow');
                if (data.following) {
                    button.text('Suivi');
                } else {
                    button.text('Suivre');
                }
            },
            error: function(xhr, status, error) {
                console.log('Error: ' + error);
            }
        });
    });
});



 // partage
// Fonction pour ouvrir le popup
function openPopup(postId) {
    var popup = document.querySelector('.popup.popup-' + postId);
    if (popup) {
        popup.style.display = "block";
    }
}

// Fonction pour fermer le popup
function closePopup(postId) {
    var popup = document.querySelector('.popup.popup-' + postId);
    if (popup) {
        popup.style.display = "none";
    }
}