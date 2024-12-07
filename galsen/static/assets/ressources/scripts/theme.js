/*==================== DARK/LIGHT THEME ====================*/
const themeButton = document.getElementById('theme-button');
const darkTheme = 'dark-theme';
const iconTheme = 'fa-moon-o'; // Classe pour l'icône de thème sombre

// Récupérer les préférences enregistrées de l'utilisateur
const selectedTheme = localStorage.getItem('selected-theme');
const selectedIcon = localStorage.getItem('selected-icon');

// Fonction pour obtenir le thème actuel
const getCurrentTheme = () => document.body.classList.contains(darkTheme) ? 'dark' : 'light';
// Fonction pour obtenir l'icône actuelle
const getCurrentIcon = () => themeButton.querySelector('.active').classList.contains('fa-moon-o') ? 'fa-moon-o' : 'fa-sun-o';

// Appliquer les préférences sauvegardées si disponibles
if (selectedTheme) {
    document.body.classList.toggle(darkTheme, selectedTheme === 'dark');
    themeButton.querySelector('span.fa-sun-o').classList.toggle('active', selectedIcon === 'fa-sun-o');
    themeButton.querySelector('span.fa-moon-o').classList.toggle('active', selectedIcon === 'fa-moon-o');
}

// Ajouter un gestionnaire d'événement pour activer/désactiver le thème
themeButton.addEventListener('click', () => {
    // Basculer entre le thème sombre et clair
    document.body.classList.toggle(darkTheme);

    // Basculer entre les icônes actives
    themeButton.querySelector('span.fa-sun-o').classList.toggle('active');
    themeButton.querySelector('span.fa-moon-o').classList.toggle('active');

    // Sauvegarder les préférences dans le localStorage
    localStorage.setItem('selected-theme', getCurrentTheme());
    localStorage.setItem('selected-icon', getCurrentIcon());
});
