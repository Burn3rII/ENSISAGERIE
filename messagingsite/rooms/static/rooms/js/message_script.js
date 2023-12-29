var last_message_date_server = "0";
var last_message_date_client = "0";
var message_number = 10;

function loadMessages() {
    const roomId = document.querySelector('script[data-room-id]').getAttribute('data-room-id');

    $.ajax({
        url: "/rooms/load_messages/",
        type: "GET",
        data: { 
            room_id: roomId,
            message_number: message_number,
        },
        success: function (data) {
            $("#messages").html(data);
        },
    });

    last_message_date_client = last_message_date_server;
}

function lastMessageDate() {
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
                
                message_number ++;
                lastMessageDate();
                loadMessages();
    
                // Pour tout de suite mettre à jour les messages
                // après un envoie de message
            },
        });
    }    
}

$(document).ready(function() {
    // Charger les messages dès le départ
    lastMessageDate();
    loadMessages();
    
    setInterval(function () {
        
        lastMessageDate();
      
        if (last_message_date_server !== last_message_date_client) {
            loadMessages();
        }
        
    }, 500);
    
    $('#messageForm').on('submit', function(event) {
        event.preventDefault();
        sendMessage();
    });

    $('seeMoreForm').on('submit', function(event) {
        event.preventDefault();
        message_number += 10;
        loadMessages();
    });
});