document.addEventListener('DOMContentLoaded', function() {
  // Stocke la position actuelle dans un cookie lors du chargement de la page
  document.cookie = 'scrollPos=' + window.scrollY + ';path=/';
});

// ================ Bouton Retour ==============
document.getElementById('boutonRetour').addEventListener('click', function() {
  // Récupère la position de défilement à partir du cookie
  var scrollPos = parseInt(getCookie('scrollPos')) || 0;

  // Vérifie si la page précédente contient un formulaire
  var previousPageUrl = document.referrer;
  var containsForm = checkForForm(previousPageUrl);

  if (containsForm) {
      // Si la page précédente contient un formulaire, utilise history.go(-2) pour revenir à la page précédente de la page contenant le formulaire
      history.go(-2);
  } else {
      // Restaure la position de défilement
      window.scrollTo(0, scrollPos);
      // Utilise history.back() pour revenir à la page précédente
      history.back();
  }
});

// Fonction pour obtenir la valeur d'un cookie
function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length === 2) return parts.pop().split(";").shift();
}

// Fonction pour vérifier si une page contient un formulaire
function checkForForm(url) {
  // Liste des URL qui contiennent des formulaires
  var formPages = [
      '/update_post',
      '/page-avec-formulaire-2',
      // Ajoutez d'autres URL de pages avec des formulaires au besoin
  ];

  // Vérifie si l'URL de la page précédente est dans la liste des pages avec des formulaires
  return formPages.includes(url);
}
