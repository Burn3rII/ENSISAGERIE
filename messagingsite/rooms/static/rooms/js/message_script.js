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
}

$(document).ready(function() {
    // Charger les messages dès le départ
    loadMessages();
    
    setInterval(function () {
        loadMessages();
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
    const message = messageInput.val();

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

            loadMessages(); 
            // Pour tout de suite mettre à jour les messages
            // après un envoie
        },
    });
}
