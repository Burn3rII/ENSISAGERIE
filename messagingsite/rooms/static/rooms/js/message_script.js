var message_number_server = 0;
var message_number_client = 0;
var message_shown_offset = 10;
var message_shown_number = message_shown_offset;
var message_shown_status = "fixed";
let queue = Promise.resolve();

function addToQueue(task) {
    queue = queue.then(() => task());
}

function loadMessages() {
    const roomId = document.querySelector('script[data-room-id]').getAttribute('data-room-id');
    //message_shown_number += message_number_server - message_number_client;

    $.ajax({
        url: "/rooms/load_messages/",
        type: "GET",
        data: { 
            room_id: roomId,
            message_number: message_shown_number,
        },
        success: function (data) {
            $("#messages").html(data);
            message_number_client = message_number_server;
        },
        
    });
    
}

function loadAllMessages() {
    const roomId = document.querySelector('script[data-room-id]').getAttribute('data-room-id');
    message_shown_number = message_number_server;

    $.ajax({
        url: "/rooms/load_all_messages/",
        type: "GET",
        data: { 
            room_id: roomId,
        },
        success: function (data) {
            $("#messages").html(data);
            message_number_client = message_number_server;
        },
    });

}

function serverMessageNumber() {
    const roomId = document.querySelector('script[data-room-id]').getAttribute('data-room-id');

    $.ajax({
        url: "/rooms/get_message_number/",
        type: "GET",
        data: { room_id: roomId },
        success: function (data) {
            message_number_server = data.message_number;
        },
    });
}

function moreShownMessageNumber() {
    if (message_shown_number + message_shown_offset < message_number_server){
        message_shown_number += message_shown_offset;
        
    } else {
        message_shown_number = message_number_server;
    }
}

function lessShownMessageNumber() {
    if (message_shown_number - message_shown_offset > message_shown_offset){
        message_shown_number -= message_shown_offset;
    } else {
        message_shown_number = message_shown_offset;
    }
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
                addToQueue(async () => {
                    messageInput.val("");
                    serverMessageNumber();
                    
                    //message_shown_number ++;

                    if (message_shown_status === "fixed"){
                        loadMessages();
                    }

                    if (message_shown_status === "all"){
                        loadAllMessages();
                    }
                    
                });
                
            },
        });
    }    
}

$(document).ready(function() {
    // Charger les messages dès le départ
    addToQueue(async () => {
        serverMessageNumber();
        loadMessages();
    });
    

    $('#messageForm').on('submit', function(event) {
        event.preventDefault();
        addToQueue(async () => {
            sendMessage();
        });
    });

    $('#seeMoreForm').on('submit', function(event) {
        event.preventDefault();      
        addToQueue(async () => {
            message_shown_status = "fixed";
            moreShownMessageNumber();
            serverMessageNumber();
            loadMessages();
        });
    });

    $('#seeLessForm').on('submit', function(event) {
        event.preventDefault();
        addToQueue(async () => {
            message_shown_status = "fixed";
            lessShownMessageNumber();
            serverMessageNumber();
            loadMessages();
        });
    });

    $('#seeAllForm').on('submit', function(event) {
        event.preventDefault();
        addToQueue(async () => {
            message_shown_status = "all";
            serverMessageNumber();
            loadAllMessages();
        });     
    });
    
    setInterval(function () {
        
        addToQueue(async () => {
            serverMessageNumber();      
      
            if (message_number_server !== message_number_client) {
                if (message_shown_status === "fixed") {
                    loadMessages();
                }
                else if (message_shown_status === "all") {
                    loadAllMessages();
                }
            }
        });
        
        
    }, 1000);
});