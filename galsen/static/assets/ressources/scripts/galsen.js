// Change Background Header (Changement du Background)
function scrollHeader(){
    const header = document.getElementById('header')

    // When the scroll is greater than 80 viewport height, add the scroll-header class to the header class to the header tag
    if(this.scrollY >= 80) header.classList.add('scroll-header'); else header.classList.remove('scroll-header')
}
window.addEventListener('scroll', scrollHeader)


// ============== Bouton Links ==========
const navlinks = document.querySelectorAll('.nav-link');
const mobilenavlinks = document.querySelectorAll('.mobile-nav-link');

// ===== Remove Bouton Links PC =====
const changeActiveLink = () => {
    navlinks.forEach(link => {
        link.classList.remove('active-link');
    })
}

navlinks.forEach(link => {
    link.addEventListener('click', () => {
        changeActiveLink();
        link.classList.add('active-link');
    })
})

// ===== Remove Bouton Links Mobile =====
const changerActiveLink = () => {
    mobilenavlinks.forEach(link => {
        link.classList.remove('active-link');
    })
}

mobilenavlinks.forEach(link => {
    link.addEventListener('click', () => {
        changerActiveLink();
        link.classList.add('active-link');
    })
})

// Slider
document.addEventListener('DOMContentLoaded', function() {
    // ... keep existing code (menu functionality)

    // Slider functionality
    const slider = document.querySelector('.slider');
    const slides = document.querySelectorAll('.slide');
    const prevBtn = document.querySelector('.slider-btn.prev');
    const nextBtn = document.querySelector('.slider-btn.next');
    
    let currentSlide = 0;
    const totalSlides = slides.length;
    
    function goToSlide(index) {
        if (index < 0) {
            currentSlide = totalSlides - 1;
        } else if (index >= totalSlides) {
            currentSlide = 0;
        } else {
            currentSlide = index;
        }
        
        slider.style.transform = `translateX(-${currentSlide * 33.333}%)`;
    }
    
    function nextSlide() {
        goToSlide(currentSlide + 1);
    }
    
    function prevSlide() {
        goToSlide(currentSlide - 1);
    }
    
    // Auto-advance slides
    let slideInterval = setInterval(nextSlide, 5000);
    
    // Reset interval when manually changing slides
    function resetInterval() {
        clearInterval(slideInterval);
        slideInterval = setInterval(nextSlide, 5000);
    }
    
    prevBtn.addEventListener('click', () => {
        prevSlide();
        resetInterval();
    });
    
    nextBtn.addEventListener('click', () => {
        nextSlide();
        resetInterval();
    });
});

// Sidebarmenus
document.addEventListener('DOMContentLoaded', function() {
    const menuBtn = document.querySelector('.menu-btn');
    const sidebar = document.querySelector('.sidebar');
    const overlay = document.querySelector('.overlay');
    const sidebarClose = document.querySelector('.sidebar-close');
    
    let isMenuOpen = false;

    // Sidebar toggle
    menuBtn.addEventListener('click', () => {
        isMenuOpen = !isMenuOpen;
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');
    });

    // Close sidebar when clicking overlay
    overlay.addEventListener('click', () => {
        isMenuOpen = false;
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
    });

    // Close sidebar with close button
    sidebarClose.addEventListener('click', () => {
        isMenuOpen = false;
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
    });
});

// Medias Carroussel
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