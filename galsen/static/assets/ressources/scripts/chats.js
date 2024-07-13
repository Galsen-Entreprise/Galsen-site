const textarea = document.querySelector("textarea");

textarea.addEventListener("input", e => {
    textarea.style.height = "59px"; // Ajustez la hauteur à une valeur légèrement inférieure à la hauteur initiale
    let scHeight = e.target.scrollHeight;
    textarea.style.height = `${Math.min(100, Math.max(60, scHeight))}px`; // Limitez la hauteur à 100px, mais assurez-vous qu'elle reste au moins à 60px
});

// Ajoutez un écouteur d'événements pour réinitialiser la hauteur lorsque le focus est perdu
textarea.addEventListener("blur", () => {
    textarea.style.height = "60px";
});


function previewFiles(inputId, previewId, maxFiles) {
    const input = document.getElementById(inputId);
    const preview = document.getElementById(previewId);

    // Réinitialiser la zone de prévisualisation
    preview.innerHTML = '';

    // Récupérer les fichiers sélectionnés
    const files = input.files;

    // Limiter le nombre de fichiers à afficher
    const filesToDisplay = Array.from(files).slice(0, maxFiles);

    // Afficher les images et vidéos
    for (const file of filesToDisplay) {
        const previewItem = document.createElement('div');
        previewItem.className = 'preview-item';

        if (file.type.startsWith('image/')) {
            const img = document.createElement('img');
            img.src = URL.createObjectURL(file);
            img.alt = file.name;

            const deleteIcon = createDeleteIcon(() => {
                preview.removeChild(previewItem);
            });

            previewItem.appendChild(img);
            previewItem.appendChild(deleteIcon);
        } else if (file.type.startsWith('video/')) {
            const video = document.createElement('video');
            video.controls = true;

            const source = document.createElement('source');
            source.src = URL.createObjectURL(file);
            source.type = file.type;

            const deleteIcon = createDeleteIcon(() => {
                preview.removeChild(previewItem);
            });

            video.appendChild(source);
            previewItem.appendChild(video);
            previewItem.appendChild(deleteIcon);
        }

        preview.appendChild(previewItem);
    }
}


function createDeleteIcon(onClick) {
    const deleteIcon = document.createElement('div');
    deleteIcon.className = 'delete-icon';
    deleteIcon.innerHTML = '&#10006;'; // Cross symbol
    deleteIcon.addEventListener('click', onClick);
    return deleteIcon;
}


// emojie
document.addEventListener('DOMContentLoaded', function () {
    const commentTextarea = document.getElementById('commentTextarea');
    const emojiPicker = document.querySelector('emoji-picker[for="commentTextarea"]');
    const emojiButton = document.getElementById('emojiButton');

    let emojiPickerVisible = false;

    if (emojiPicker) {
        emojiPicker.style.display = 'none';  // Masquer l'emoji-picker au chargement de la page

        emojiPicker.addEventListener('emoji-click', function (event) {
            // Ajouter l'emoji sélectionné au contenu du textarea
            const currentCursorPosition = commentTextarea.selectionStart;
            const emoji = event.detail.unicode;
            const newContent = commentTextarea.value.slice(0, currentCursorPosition) + emoji + commentTextarea.value.slice(currentCursorPosition);

            // Mettre à jour le contenu du textarea
            commentTextarea.value = newContent;

            // Masquer l'emoji-picker après la sélection
            emojiPicker.hide();
            emojiPickerVisible = false;

            // Restaurer le focus sur le textarea
            commentTextarea.focus();
        });

        emojiButton.addEventListener('click', function (event) {
            event.preventDefault();
            console.log('Emoji Button clicked');
            console.log('Emoji Picker:', emojiPicker);

            // Afficher ou masquer l'emoji-picker en modifiant directement l'attribut de style
            emojiPicker.style.display = (emojiPicker.style.display === 'none') ? 'block' : 'none';
            emojiPickerVisible = !emojiPickerVisible;

            if (emojiPickerVisible) {
                // Si l'emoji-picker est visible, n'autorise pas le focus sur le textarea
                commentTextarea.blur();
            } else {
                // Si l'emoji-picker est masqué, restaurer le focus sur le textarea
                commentTextarea.focus();
            }
        });

        commentTextarea.addEventListener('focus', function () {
            // Vérifier si l'origine de l'événement est le bouton emoji
            if (!emojiPickerVisible) {
                console.log('Textarea focused');
                emojiPicker.style.display = 'none';  // Masquer l'emoji-picker si le focus est sur le textarea
            }
        });

        commentTextarea.addEventListener('blur', function () {
            // Vérifier si le blur n'est pas causé par le passage au-dessus de l'emoji-picker
            if (!emojiPicker.contains(document.activeElement)) {
                console.log('Textarea blurred');
                emojiPicker.style.display = 'none';
            }
        });
    } else {
        console.error('Emoji Picker not found.');
    }
});

