var last_message_date_server = "0";
var last_message_date_client = "0";
$(document).ready(function () {

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