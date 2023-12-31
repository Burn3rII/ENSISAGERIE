$(document).ready(function() {

// Partie invitations----------------------------------------------------------
     function searchInviteUsers(searchTerm, roomId) {
        $.ajax({
            type: "GET",
            url: "/rooms/search_invite_user/",
            data: {
                search_term: searchTerm,
                room_id: roomId,
            },
            success: function(data) {
                $("#invite-user-results").html(
                data.invite_users_search_results_html);
            },
            error: function(error) {
                console.log("Erreur de requête AJAX:", error);
            }
        });
    }

    $("#invite-user-form").submit(function(event) {
        event.preventDefault();
        var searchTerm = $("#invite-user-input").val();
        const roomId = document.querySelector(
        'script[data-room-id]').getAttribute('data-room-id');
        searchInviteUsers(searchTerm, roomId);
    });

    $("#invite-user-results").on("click", ".invite-btn", function() {
        const roomId = document.querySelector(
        'script[data-room-id]').getAttribute('data-room-id');
        const userId = $(this).data('user-id');

        $.ajax({
            url: `/rooms/invite/`,
            method: "POST",
            data: {
                room_id: roomId,
                user_id: userId,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (data) {
                alert(data.message);
                var searchTerm = $("#room-search-input").val();
                searchInviteUsers(searchTerm, roomId);
            },
            error: function (error) {
                console.log("Erreur de requête AJAX:", error);
            }
        });
    });

// Partie suppression d'utilisateurs-------------------------------------------
    function searchRemoveUsers(searchTerm, roomId) {
        $.ajax({
            type: "GET",
            url: "/rooms/search_remove_user/",
            data: {
                search_term: searchTerm,
                room_id: roomId,
            },
            success: function(data) {
                $("#remove-user-results").html(data.remove_users_search_results_html);
            },
            error: function(error) {
                console.log("Erreur de requête AJAX:", error);
            }
        });
    }

    $("#remove-user-form").submit(function(event) {
        event.preventDefault();
        var searchTerm = $("#remove-user-input").val();
        const roomId = document.querySelector(
        'script[data-room-id]').getAttribute('data-room-id');
        searchRemoveUsers(searchTerm, roomId);
    });

    $("#remove-user-results").on("click", ".remove-user-btn", function() {
        const roomId = document.querySelector(
        'script[data-room-id]').getAttribute('data-room-id');
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
                var searchTerm = $("#remove-user-input").val();
                searchRemoveUsers(searchTerm, roomId);
            },
            error: function (error) {
                console.log("Erreur de requête AJAX:", error);
            }
        });
    });

// Partie demandes en attente--------------------------------------------------
    function refreshPendingRequests() {
        const roomId = document.querySelector(
        'script[data-room-id]').getAttribute('data-room-id');

        $.ajax({
            type: "GET",
            url: `/rooms/refresh_pending_requests/`,
            data: {
                room_id: roomId,
            },
            success: function(data) {
                $("#pending-requests").html(data.updated_pending_requests_html)
                ;
            },
            error: function(error) {
                console.log("Erreur de requête AJAX:", error);
            }
        });
    }

    refreshPendingRequests()

    $("#pending-requests").on("click", ".approve-request-btn", function() {
        const requestId = $(this).data('request-id'); // data() une
        // fonction de jQuery qui permet d'accéder aux valeurs des attributs
        // data-* d'un élément HTML.

        $.ajax({
            url: `/rooms/accept_pending_request/`,
            method: "POST",
            data: {
                request_id: requestId,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (data) {
                alert(data.message);
                refreshPendingRequests()
            },
            error: function (error) {
                console.log("Erreur de requête AJAX:", error);
            }
        });
    });

    $("#pending-requests").on("click", ".reject-request-btn", function() {
        const requestId = $(this).data('request-id'); // data() une
        // fonction de jQuery qui permet d'accéder aux valeurs des attributs
        // data-* d'un élément HTML.

        $.ajax({
            url: `/rooms/reject_pending_request/`,
            method: "POST",
            data: {
                request_id: requestId,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (data) {
                alert(data.message);
                refreshPendingRequests()
            },
            error: function (error) {
                console.log("Erreur de requête AJAX:", error);
            }
        });
    });
});
