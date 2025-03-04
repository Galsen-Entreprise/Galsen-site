let countryIndicatifs = {
  "Afghanistan": 93,
  "Åland Islands": 358, // Remplacez par l'indicatif approprié
  "Albania": 355,
  "Algeria": 213,
  "American Samoa": 1, // Remplacez par l'indicatif approprié
  "Andorra": 376,
  "Angola": 244,
  "Anguilla": 1, // Remplacez par l'indicatif approprié
  "Antarctica": 672,
  "Antigua and Barbuda": 1, // Remplacez par l'indicatif approprié
  "Argentina": 54,
  "Armenia": 374,
  "Aruba": 297,
  "Australia": 61,
  "Austria": 43,
  "Azerbaijan": 994,
  "Bahamas": 1, // Remplacez par l'indicatif approprié
  "Bahrain": 973,
  "Bangladesh": 880,
  "Barbados": 1, // Remplacez par l'indicatif approprié
  "Belarus": 375,
  "Belgium": 32,
  "Belize": 501,
  "Benin": 229,
  "Bermuda": 1, // Remplacez par l'indicatif approprié
  "Bhutan": 975,
  "Bolivia": 591,
  "Bosnia and Herzegovina": 387,
  "Botswana": 267,
  "Bouvet Island": 47,
  "Brazil": 55,
  "British Indian Ocean Territory": 246,
  "Brunei Darussalam": 673,
  "Bulgaria": 359,
  "Burkina Faso": 226,
  "Burundi": 257,
  "California": 1,
  "Cambodia": 855,
  "Cameroon": 237,
  "Canada": 1,
  "Cape Verde": 238,
  "Cayman Islands": 1, // Remplacez par l'indicatif approprié
  "Central African Republic": 236,
  "Chad": 235,
  "Chile": 56,
  "China": 86,
  "Christmas Island": 61,
  "Cocos (Keeling) Islands": 61,
  "Colombia": 57,
  "Comoros": 269,
  "Congo": 242,
  "Congo, The Democratic Republic of the": 243,
  "Cook Islands": 682,
  "Costa Rica": 506,
  "Cote D'Ivoire": 225,
  "Croatia": 385,
  "Cuba": 53,
  "Cyprus": 357,
  "Czech Republic": 420,
  "Denmark": 45,
  "Djibouti": 253,
  "Dominica": 1, // Remplacez par l'indicatif approprié
  "Dominican Republic": 1, // Remplacez par l'indicatif approprié
  "Ecuador": 593,
  "Egypt": 20,
  "El Salvador": 503,
  "Equatorial Guinea": 240,
  "Eritrea": 291,
  "Estonia": 372,
  "Ethiopia": 251,
  "Falkland Islands (Malvinas)": 500,
  "Faroe Islands": 298,
  "Fiji": 679,
  "Finland": 358,
  "France": 33,
  "French Guiana": 594,
  "French Polynesia": 689,
  "French Southern Territories": 262,
  "Gabon": 241,
  "Gambia": 220,
  "Georgia": 995,
  "Germany": 49,
  "Ghana": 233,
  "Gibraltar": 350,
  "Greece": 30,
  "Greenland": 299,
  "Grenada": 1, // Remplacez par l'indicatif approprié
  "Guadeloupe": 590,
  "Guam": 1, // Remplacez par l'indicatif approprié
  "Guatemala": 502,
  "Guernsey": 44,
  "Guinea": 224,
  "Guinea-Bissau": 245,
  "Guyana": 592,
  "Haiti": 509,
  "Heard Island and Mcdonald Islands": 672,
  "Holy See (Vatican City State)": 379,
  "Honduras": 504,
  "Hong Kong": 852,
  "Hungary": 36,
  "Iceland": 354,
  "India": 91,
  "Indonesia": 62,
  "Iran, Islamic Republic Of": 98,
  "Iraq": 964,
  "Ireland": 353,
  "Isle of Man": 44,
  "Israel": 972,
  "Italy": 39,
  "Jamaica": 1, // Remplacez par l'indicatif approprié
  "Japan": 81,
  "Jersey": 44,
  "Jordan": 962,
  "Kazakhstan": 7,
  "Kenya": 254,
  "Kiribati": 686,
  "Korea, Democratic People's Republic of": 850,
  "Korea, Republic of": 82,
  "Kuwait": 965,
  "Kyrgyzstan": 996,
  "Lao People's Democratic Republic": 856,
  "Latvia": 371,
  "Lebanon": 961,
  "Lesotho": 266,
  "Liberia": 231,
  "Libyan Arab Jamahiriya": 218,
  "Liechtenstein": 423,
  "Lithuania": 370,
  "Luxembourg": 352,
  "Macao": 853,
  "Macedonia, The Former Yugoslav Republic of": 389,
  "Madagascar": 261,
  "Malawi": 265,
  "Malaysia": 60,
  "Maldives": 960,
  "Mali": 223,
  "Malta": 356,
  "Marshall Islands": 692,
  "Martinique": 596,
  "Mauritania": 222,
  "Mauritius": 230,
  "Mayotte": 262,
  "Mexico": 52,
  "Micronesia, Federated States of": 691,
  "Moldova, Republic of": 373,
  "Monaco": 377,
  "Mongolia": 976,
  "Montserrat": 1, // Remplacez par l'indicatif approprié
  "Morocco": 212,
  "Mozambique": 258,
  "Myanmar": 95,
  "Namibia": 264,
  "Nauru": 674,
  "Nepal": 977,
  "Netherlands": 31,
  "Netherlands Antilles": 599,
  "New Caledonia": 687,
  "New Zealand": 64,
  "Nicaragua": 505,
  "Niger": 227,
  "Nigeria": 234,
  "Niue": 683,
  "Norfolk Island": 672,
  "Northern Mariana Islands": 1, // Remplacez par l'indicatif approprié
  "Norway": 47,
  "Oman": 968,
  "Pakistan": 92,
  "Palau": 680,
  "Palestinian Territory, Occupied": 970,
  "Panama": 507,
  "Papua New Guinea": 675,
  "Paraguay": 595,
  "Peru": 51,
  "Philippines": 63,
  "Pitcairn": 872, // Remplacez par l'indicatif approprié
  "Poland": 48,
  "Portugal": 351,
  "Puerto Rico": 1, // Remplacez par l'indicatif approprié
  "Qatar": 974,
  "Reunion": 262,
  "Romania": 40,
  "Russian Federation": 7,
  "Rwanda": 250,
  "Saint Helena": 290,
  "Saint Kitts and Nevis": 1, // Remplacez par l'indicatif approprié
  "Saint Lucia": 1, // Remplacez par l'indicatif approprié
  "Saint Pierre and Miquelon": 508,
  "Saint Vincent and the Grenadines": 1, // Remplacez par l'indicatif approprié
  "Samoa": 685,
  "San Marino": 378,
  "Sao Tome and Principe": 239,
  "Saudi Arabia": 966,
  "Senegal": 221,
  "Seychelles": 248,
  "Sierra Leone": 232,
  "Singapore": 65,
  "Slovakia": 421,
  "Slovenia": 386,
  "Solomon Islands": 677,
  "Somalia": 252,
  "South Africa": 27,
  "South Georgia and the South Sandwich Islands": 500,
  "Spain": 34,
  "Sri Lanka": 94,
  "Sudan": 249,
  "Suriname": 597,
  "Svalbard and Jan Mayen": 47,
  "Swaziland": 268,
  "Sweden": 46,
  "Switzerland": 41,
  "Syrian Arab Republic": 963,
  "Taiwan, Province of China": 886,
  "Tajikistan": 992,
  "Tanzania, United Republic of": 255,
  "Thailand": 66,
  "Timor-Leste": 670,
  "Togo": 228,
  "Tokelau": 690,
  "Tonga": 676,
  "Trinidad and Tobago": 1, // Remplacez par l'indicatif approprié
  "Tunisia": 216,
  "Turkey": 90,
  "Turkmenistan": 993,
  "Turks and Caicos Islands": 1, // Remplacez par l'indicatif approprié
  "Tuvalu": 688,
  "Uganda": 256,
  "Ukraine": 380,
  "United Arab Emirates": 971,
  "United Kingdom": 44,
  "United States": 1,
  "United States Minor Outlying Islands": 1, // Remplacez par l'indicatif approprié
  "Uruguay": 598,
  "Uzbekistan": 998,
  "Vanuatu": 678,
  "Venezuela": 58,
  "Viet Nam": 84,
  "Virgin Islands, British": 1, // Remplacez par l'indicatif approprié
  "Virgin Islands, U.S.": 1, // Remplacez par l'indicatif approprié
  "Wallis and Futuna": 681,
  "Western Sahara": 212,
  "Yemen": 967,
  "Zambia": 260,
  "Zimbabwe": 263,
};

let countries = Object.keys(countryIndicatifs);

// Référence à l'élément d'entrée du pays
let input = document.getElementById("countryInput");

// Référence à l'élément d'indicatif
let indicatifInput = document.getElementById("indicatif");
let indicatifSpan = document.querySelector(".input-group .bar");

// Exécuter la fonction updateIndicatif lors du changement de la valeur du champ de saisie du pays
input.addEventListener("input", updateIndicatif);

// Fonction pour mettre à jour l'indicatif en fonction du pays sélectionné
function updateIndicatif() {
  let selectedCountry = input.value.trim();
  let indicatifValue = countryIndicatifs[selectedCountry] || "";
  indicatifInput.value = indicatifValue;

  // Mettez à jour le texte de l'élément span à côté de l'indicatif si nécessaire
  indicatifSpan.innerText = indicatifValue ? `Indicatif: +${indicatifValue}` : "";
}

// Fonction pour gérer la liste déroulante des pays
input.addEventListener("input", () => {
  let inputValue = input.value.toLowerCase();
  let matchedCountries = countries.filter((country) =>
    country.toLowerCase().includes(inputValue)
  );

  // clear the list
  removeElements();

  // populate the list with matched countries
  matchedCountries.forEach((country) => {
    let listItem = document.createElement("li");
    listItem.classList.add("list-items");
    listItem.style.cursor = "pointer";
    listItem.setAttribute("onclick", `displayNames('${country}')`);

    let matchIndex = country.toLowerCase().indexOf(inputValue);
    let matchPart = country.substring(matchIndex, matchIndex + inputValue.length);
    let restPart = country.substring(matchIndex + inputValue.length);

    listItem.innerHTML = `<b>${matchPart}</b>${restPart}`;
    document.querySelector(".list").appendChild(listItem);
  });
});

function displayNames(value) {
  input.value = value;
  removeElements();
  updateIndicatif();
}

function removeElements() {
  let items = document.querySelectorAll(".list-items");
  items.forEach((item) => {
    item.remove();
  });
}

// Exécuter la fonction updateIndicatif lors du chargement de la page
updateIndicatif();