$(document).ready(function() {

// Partie vos salons-----------------------------------------------------------
    function refreshYourRooms() {
        $.ajax({
            type: "GET",
            url: `/rooms/refresh_your_rooms/`,
            success: function(data) {
                $("#your-rooms").html(data.updated_your_rooms_html);
            },
            error: function(error) {
                console.log("Erreur de requête AJAX:", error);
            }
        });
    }

    refreshYourRooms()

    $("#your-rooms").on("click", ".remove-user-btn", function() {
        const roomId = $(this).data('room-id');
        const userId = $(this).data('user-id');

        $.ajax({
            url: `/rooms/remove_user/`,
            method: "POST",
            data: {
                room_id: roomId,
                user_id: userId,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (data) {
                alert(data.message);
                refreshYourRooms();
            },
            error: function (error) {
                console.log("Erreur de requête AJAX:", error);
            }
        });
    });

// Partie invitations recues---------------------------------------------------

    function refreshRoomsInvitations() {
        $.ajax({
            type: "GET",
            url: `/rooms/refresh_rooms_invitations/`,
            success: function(data) {
                $("#rooms-invitations").html(data.updated_rooms_invitations_html);
            },
            error: function(error) {
                console.log("Erreur de requête AJAX:", error);
            }
        });
    }

    refreshRoomsInvitations()

    $("#rooms-invitations").on("click", ".accept-invitation-btn", function() {
        const invitationId = $(this).data('invitation-id'); // data() une
        // fonction de jQuery qui permet d'accéder aux valeurs des attributs
        // data-* d'un élément HTML.

        $.ajax({
            url: `/rooms/accept_invitation/`,
            method: "POST",
            data: {
                invitation_id: invitationId,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (data) {
                alert(data.message);
                refreshRoomsInvitations();
                refreshYourRooms();
            },
            error: function (error) {
                console.log("Erreur de requête AJAX:", error);
            }
        });
    });

    $("#rooms-invitations").on("click", ".reject-invitation-btn", function() {
        const invitationId = $(this).data('invitation-id'); // data() une
        // fonction de jQuery qui permet d'accéder aux valeurs des attributs
        // data-* d'un élément HTML.

        $.ajax({
            url: `/rooms/reject_invitation/`,
            method: "POST",
            data: {
                invitation_id: invitationId,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (data) {
                alert(data.message);
                refreshRoomsInvitations();
            },
            error: function (error) {
                console.log("Erreur de requête AJAX:", error);
            }
        });
    });

// Partie vos requêtes---------------------------------------------------------
    function refreshYourRequests() {
        $.ajax({
            type: "GET",
            url: `/rooms/refresh_your_requests/`,
            success: function(data) {
                $("#your-requests").html(data.updated_your_requests_html);
            },
            error: function(error) {
                console.log("Erreur de requête AJAX:", error);
            }
        });
    }

    refreshYourRequests()

// Partie demandes acceptées---------------------------------------------------
    function refreshAcceptedRequests() {
        $.ajax({
            type: "GET",
            url: `/rooms/refresh_accepted_requests/`,
            success: function(data) {
                $("#accepted_requests").html(data.updated_accepted_requests_html);
            },
            error: function(error) {
                console.log("Erreur de requête AJAX:", error);
            }
        });
    }

    refreshAcceptedRequests()

    $("#accepted_requests").on("click", ".delete-accepted-request-btn",
    function() {
        const requestId = $(this).data('request-id'); // data() une
        // fonction de jQuery qui permet d'accéder aux valeurs des attributs
        // data-* d'un élément HTML.

        $.ajax({
            url: `/rooms/delete_accepted_request/`,
            method: "POST",
            data: {
                request_id: requestId,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (data) {
                refreshAcceptedRequests();
            },
            error: function (error) {
                console.log("Erreur de requête AJAX:", error);
            }
        });
    });

// Partie recherche de salons--------------------------------------------------
    var searchTermRoom;

    function searchRoom() {
        $.ajax({
            type: "GET",
            url: `/rooms/search_room/`,
            data: {
                search_term: searchTermRoom,
            },
            success: function(data) {
                $("#room-search-results").html(data.rooms_search_results_html);
            },
            error: function(error) {
                console.log("Erreur de requête AJAX:", error);
            }
        });
    }

    $("#room-search-form").submit(function(event) {
        event.preventDefault();
        searchTermRoom = $("#room-search-input").val();
        searchRoom();
        refreshYourRooms();
        refreshRoomsInvitations();
    });

    $("#room-search-results").on("click", ".join-room-btn", function() {
        const roomId = $(this).data('room-id');

        $.ajax({
            url: `/rooms/join_room/`,
            method: "POST",
            data: {
                room_id: roomId,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (data) {
                alert(data.message);
                searchRoom();
                refreshYourRooms();
            },
            error: function (error) {
                console.log("Erreur de requête AJAX:", error);
            }
        });
    });

    $("#room-search-results").on("click", ".request-to-join-btn", function() {
        const roomId = $(this).data('room-id'); // data() une fonction de
        // jQuery qui permet d'accéder aux valeurs des attributs data-* d'un
        // élément HTML.

        $.ajax({
            url: `/rooms/request_to_join/`,
            method: "POST",
            data: {
                room_id: roomId,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (data) {
                alert(data.message);
                var searchTerm = $("#room-search-input").val();
                searchRoom(searchTerm);
                refreshYourRequests();
            },
            error: function (error) {
                console.log("Erreur de requête AJAX:", error);
            }
        });
    });

// Partie carrousel------------------------------------------------------------
    var staticUrl = document.getElementById('carrousel').getAttribute(
    'data-static-url');
    var imageDescriptionElement = document.getElementById('image-description');
    var displayedImages = []; // Tableau pour stocker les indices des images
    // déjà affichées

    $.getJSON(staticUrl + 'json/images_descriptions.json',
    function(descriptions) {
        changePicture();

        setInterval(function() {
            $("#carrousel").fadeOut(1000, changePicture);
        }, 20000);

        function getRandomImageIndex() {
            var randomIndex;
            do {
                randomIndex = Math.floor(Math.random() * 12);
            } while (displayedImages.includes(randomIndex));

            displayedImages.push(randomIndex);

            // Si toutes les images ont été affichées, réinitialiser le tableau
            if (displayedImages.length === 12) {
                displayedImages = [];
            }

            return randomIndex;
        }

        function changePicture() {
            var randomImageIndex = getRandomImageIndex();
            var imageUrl = staticUrl + "images/singes" + randomImageIndex +
            ".jpg";
            var description = descriptions["singes" + randomImageIndex +
            ".jpg"];

            $("#carrousel").attr("src", imageUrl);
            $("#carrousel").fadeIn(1000);
            imageDescriptionElement.innerText = description;
        }
    });
});




