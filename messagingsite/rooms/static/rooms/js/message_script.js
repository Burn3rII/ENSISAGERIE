var last_message_date_server = "0";
var last_message_date_client = "0";

function loadMessages() {
    const roomId = document.querySelector('script[data-room-id]').getAttribute('data-room-id');

    $.ajax({
        url: "/rooms/load_messages/",
        type: "GET",
        data: { room_id: roomId },
        success: function (data) {
            $("#messages").html(data);
        },
    });

    last_message_date_client = last_message_date_server;
}

function last_message_date() {
    const roomId = document.querySelector('script[data-room-id]').getAttribute('data-room-id');

    $.ajax({
        url: "/rooms/last_message_date/",
        type: "GET",
        data: { room_id: roomId },
        success: function (data) {
            last_message_date_server = data.last_message_date;
        },
    });
}

$(document).ready(function() {
    // Charger les messages dès le départ
    last_message_date();
    loadMessages();
    
    setInterval(function () {
        
        last_message_date();
      
        if (last_message_date_server !== last_message_date_client) {
            loadMessages();
        }
        
    }, 1500);
    
    $('#messageForm').on('submit', function(event) {
        event.preventDefault();
        sendMessage();
    });
});

function sendMessage() {
    const roomId = document.querySelector('script[data-room-id]').getAttribute('data-room-id');
    const csrfToken = document.querySelector('script[data-csrf-token]').getAttribute('data-csrf-token');

    const messageInput = $("#messageInput");
    let message = messageInput.val();
    message = message.trim();

    if (message !== "") {
        $.ajax({
            url: "/rooms/send_message/",
            type: "POST",
            data: {
                room_id: roomId,
                message: message,
                csrfmiddlewaretoken: csrfToken,
            },
            success: function () {
                messageInput.val("");
    
                last_message_date();
                loadMessages();
    
                // Pour tout de suite mettre à jour les messages
                // après un envoie de message
            },
        });
    }    
}
/*
$(document).ready(function () {
    // Fonction pour générer un tableau d'emojis basé sur les Unicode codepoints
    function generateEmojis() {
        const emojis = [];

        // Boucle à travers les Unicode codepoints pour les emojis et les intègre dans le tableau
        for (let i = 0x1F600; i <= 0x1F64F; i++) {
            emojis.push(String.fromCodePoint(i));
        }

        return emojis;
    }

    // Fonction pour afficher les emojis dans un conteneur spécifié
    function displayEmojis(containerId, emojis) {
        const emojiContainer = $('#' + containerId);
        emojiContainer.empty(); // Vide le conteneur avant l'affichage des emojis

        // Affiche chaque emoji dans le conteneur
        emojis.forEach(emoji => {
            const emojiElement = $('<span class="emoji">').text(emoji);
            emojiContainer.append(emojiElement);

            // AJoute des click event handler à chaque emoji
            emojiElement.on('click', function () {
                // Récupère le texte actuel dans le champ de saisie
                const currentText = $('#messageInput').val();

                // Ajoute l'emoji cliqué au champ de saisie
                $('#messageInput').val(currentText + emoji);
            });
        });
    }

    // Ajoute un event handler pour le bouton emoji qui affiche les emojis
    $('#emojiButton').on('click', function () {
        const emojis = generateEmojis();
        displayEmojis('emojiContainer', emojis);
    });
});
*/

/*
$(document).ready(function () {
    const emojiButton = $('#emojiButton');
    const emojiContainer = $('#emojiContainer');
    const messageInput = $('#messageInput');

    emojiButton.click(function () {
        emojiContainer.toggle();
    });

    // Add event listener to each emoji button
    $('.emojiButtons').click(function () {
        const emoji = $(this).data('emoji');
        // Ajoute l'emoji sélectionné au champ de saisie
        $("#messageInput").val($("#messageInput").val() + selectedEmoji);
    });

});
*/






$(document).ready(function () {
    const emojiButton = $('#emojiButton');
    const emojiContainer = $('#emojiContainer');
    const messageInput = $('#messageInput');

    // Populate category buttons dynamically
    function populateCategoryButtons(emojiData) {
        const categoryButtonsContainer  = $('#categoryButtonsContainer');
        categoryButtonsContainer .empty(); // Clear previous content

        $.each(emojiData, function (category, emojis) {
            const button = $('<button>', {
                type: 'button',
                class: 'categoryButton',
                'data-category': category,
                text: category,
            });

            categoryButtonsContainer .append(button);
        });
    }

    // Populate emoji buttons dynamically
    function populateEmojiButtons(emojis) {
        const emojiList = $('#emojiContainer');
        emojiList.empty(); // Clear previous content
        emojiList.hide();  // Hide emoji container until it is populated

        // Check if 'emojis' is an array
        if (Array.isArray(emojis)) {
            $.each(emojis, function (index, emoji) {
                const button = $('<button>', {
                    type: 'button',
                    class: 'emojiButtons',
                    'data-emoji': emoji.emoji,
                    text: emoji.emoji + ' - ' + emoji.name,
                });

                emojiList.append(button);
            });
        } else {
            console.error('Invalid format for emojis:', emojis);
        }

        // Show the emoji container after populating the buttons
        emojiList.show();
    }

    // Fetch emoji data using AJAX
    $.ajax({
        url: JSONfile,
        method: 'GET',
        dataType: 'json',
        success: function (emojiData) {
            // Save emojiData in a global variable for later use
            window.emojiData = emojiData;

            // Populate category buttons
            populateCategoryButtons(emojiData);

            // Add event listener to each category button
            $(document).on('click', '.categoryButton', function () {
                console.log('Category button clicked');
                const categoryIndex = $(this).data('category');

                if (typeof categoryIndex === 'number' && emojiData[categoryIndex]) {
                    const category = emojiData[categoryIndex];

                    if (category.emojis && Array.isArray(category.emojis)) {
                        populateEmojiButtons(category.emojis);
                        emojiContainer.show(); // Show the emoji container when a category button is clicked
                        $('#emojiContainer').siblings('.categoryButton').show(); // Show category buttons
                    } else {
                        console.error('Invalid format for category emojis:', category);
                    }
                } else {
                    console.error('Invalid category index:', categoryIndex);
                }
            });

            // Toggle visibility of emojiContainer
            emojiButton.click(function () {
                console.log('Emoji button clicked');
                if (emojiContainer.is(':visible')) {
                    console.log('Emoji container is visible, hiding');
                    emojiContainer.hide();
                } else {
                    console.log('Emoji container is hidden, showing');
                    emojiContainer.show();
                }
            });

            // Add event listener to each emoji button
            $(document).on('click', '.emojiButtons', function () {
                console.log('Emoji button clicked');
                const emoji = $(this).data('emoji');
                messageInput.val(messageInput.val() + emoji);
            });
        },
        error: function (error) {
            console.error('Error fetching emoji data:', error);
        }
    });
});

