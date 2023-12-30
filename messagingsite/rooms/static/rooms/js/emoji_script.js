$(document).ready(function () {
    const emojiButton = $('#emojiButton');
    const categoryButtonsContainer = $('#categoryButtonsContainer');
    const emojiContainer = $('#emojiContainer');
    const messageInput = $('#messageInput');

    // Permet de conserver l'index de la catégorie cliquée précédemment
    let lastClickedCategory = null;

    // Rempli les catégories de boutons dynamiquement
    function populateCategoryButtons(emojiData) {
        categoryButtonsContainer.empty(); // Efface le précédent contenu

        $.each(emojiData, function (index, category) {
            const button = $('<button>', {
                type: 'button',
                class: 'categoryButton',
                'data-category': index,
                text: category.name, // Rempli le texte des boutons des catégories en fonction de la propriété "name"
            });
            categoryButtonsContainer.append(button);
        });
    }

    // Peuple les boutons d'emojis dynamiquement
    function populateEmojiButtons(emojis) {
        emojiContainer.empty(); // Efface le précédent contenu
        emojiContainer.hide();  // Cache le conteneur des emojis jusqu'à ce qu'il soit rempli

        // Vérifie que 'emojis' est un array
        if (Array.isArray(emojis)) {
            $.each(emojis, function (index, emoji) {
                const button = $('<button>', {
                    type: 'button',
                    class: 'emojiButtons',
                    'data-emoji': emoji.emoji,
                    text: emoji.emoji, // Rempli le texte des boutons d'emojis en fonction de la propriété "emoji"
                });

                emojiContainer.append(button);
            });
        } else {
            console.error('Invalid format for emojis:', emojis);
        }
    }

    // Récupère le fichier JSON contenant les emojis en utilisant AJAX
    $.ajax({
        url: JSONfile,
        method: 'GET',
        dataType: 'json',
        success: function (emojiData) {
            // Sauvegarde emojiData dans une variable globale pour une utilisation ultérieure
            window.emojiData = emojiData;

            // Peuple les boutons de catégorie
            populateCategoryButtons(emojiData);

            // Ajoute un event listener à chaque bouton de catégorie
            $(document).on('click', '.categoryButton', function () {
                console.log('Category button clicked');
                const categoryIndex = $(this).data('category');
                // Vérifie que l'index de la catégorie est bien un nombre et que categoryIndex existe dans emojiData
                if (typeof categoryIndex === 'number' && emojiData[categoryIndex]) {
                    const category = emojiData[categoryIndex];
                    // Vérifie que la catégorie contient bien des emojis et que l'array est bien formaté
                    if (category.emojis && Array.isArray(category.emojis)) {
                        if (lastClickedCategory === categoryIndex) {
                            // Si la même catégorie est cliquée, cache le conteneur des emojis
                            console.log('Emoji container is visible, hiding');
                            emojiContainer.hide();
                            lastClickedCategory = null;  // Réinitialise la variable lastClickedCategory
                        } else {
                            // Si une autre catégorie est cliquée, affiche et peuple directement le conteneur des emojis
                            console.log('Emoji container is changing categories');
                            populateEmojiButtons(category.emojis);
                            emojiContainer.show(); // Affiche le conteneur des emojis
                            lastClickedCategory = categoryIndex;  // Met à jour la variable lastClickedCategory
                        }
                    } else {
                        console.error('Invalid format for category emojis:', category);
                    }
                } else {
                    console.error('Invalid category index:', categoryIndex);
                }
            });

            // Gère la visibilité du conteneur des emojis
            emojiButton.click(function () {
                console.log('Before click: ', messageInput.val());
                console.log('Emoji button clicked');
                if (categoryButtonsContainer.is(':visible')) {
                    if (emojiContainer.is(':visible')) {
                        console.log('Emoji container is visible, hiding');
                        emojiContainer.hide();
                    }
                    console.log('Category container is visible, hiding');
                    categoryButtonsContainer.hide();
                } else {
                    console.log('Category container is hidden, showing');
                    categoryButtonsContainer.show();
                    lastClickedCategory = null;  // Réinitialise la variable lastClickedCategory
                }
            });

            // Ajoute un event listener à chaque bouton d'emoji
            $(document).on('click', '.emojiButtons', function () {
                console.log('Emoji button clicked');
                const emoji = $(this).data('emoji');
                messageInput.val(messageInput.val() + emoji);
            });

            // Cache les conteneurs après avoir configuré les event listeners
            console.log('First loading of the page, emojis is hiding');
            emojiContainer.hide();
            console.log('First loading of the page, Category container is hiding');
            categoryButtonsContainer.hide();
        },
        error: function (error) {
            console.error('Error fetching emoji data:', error);
        }
    });
});