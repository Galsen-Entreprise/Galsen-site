// Gestion des aperçus d'image et de vidéo
function previewImage(input, previewId) {
    const preview = document.getElementById(previewId);
    const file = input.files[0];

    if (file) {
        const reader = new FileReader();

        reader.onload = function (e) {
            preview.innerHTML = `<img src="${e.target.result}" alt="Image Preview">`;
        };

        reader.readAsDataURL(file);
    } else {
        preview.innerHTML = `<p>Aucune image sélectionnée</p>`;
    }
}

function previewVideo(input, previewId) {
    const preview = document.getElementById(previewId);
    const file = input.files[0];

    if (file) {
        const reader = new FileReader();

        reader.onload = function (e) {
            preview.innerHTML = `<video controls>
                                    <source src="${e.target.result}" type="${file.type}">
                                    Votre navigateur ne supporte pas les vidéos.
                                 </video>`;
        };

        reader.readAsDataURL(file);
    } else {
        preview.innerHTML = `<p>Aucune vidéo sélectionnée</p>`;
    }
}

document.getElementById("image").addEventListener("change", function () {
    previewImage(this, "imagePreview");
});

document.getElementById("video").addEventListener("change", function () {
    previewVideo(this, "videoPreview");
});