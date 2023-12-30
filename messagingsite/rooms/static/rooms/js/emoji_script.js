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
