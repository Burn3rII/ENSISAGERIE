var message_number_server = 0;
var message_number_client = 0;
var message_shown_offset = 10;
var message_shown_number = message_shown_offset;
var message_shown_status = "auto";

function loadMessages() {
    const roomId = document.querySelector('script[data-room-id]').getAttribute('data-room-id');
    message_shown_number += message_number_server - message_number_client;

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
        url: "/rooms/message_number/",
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
                messageInput.val("");
                
                if (message_shown_status === "auto"){
                    serverMessageNumber();
                    loadMessages();
                }

                if (message_shown_status === "all"){
                    serverMessageNumber();
                    loadAllMessages();
                }
            },
        });
    }    
}

$(document).ready(function() {
    // Charger les messages dès le départ
    serverMessageNumber();
    loadMessages();
    
    setInterval(function () {
        
        serverMessageNumber();       
      
        if (message_number_server !== message_number_client) {
            if (message_shown_status === "auto") {
                loadMessages();
            }
            else if (message_shown_status === "all") {
                loadAllMessages();
            }
        }
        
    }, 1500);
    
    $('#messageForm').on('submit', function(event) {
        event.preventDefault();
        sendMessage();
    });

    $('#seeMoreForm').on('submit', function(event) {
        event.preventDefault();
        message_shown_status = "auto";
        moreShownMessageNumber();
        serverMessageNumber();
        loadMessages();
    });

    $('#seeLessForm').on('submit', function(event) {
        event.preventDefault();
        message_shown_status = "auto";
        lessShownMessageNumber();
        serverMessageNumber();
        loadMessages();
    });

    $('#seeAllForm').on('submit', function(event) {
        event.preventDefault();
        message_shown_status = "all";
        serverMessageNumber();
        loadAllMessages();
    });
});

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
