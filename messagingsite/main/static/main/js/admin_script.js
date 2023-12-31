$(document).ready(function() {

// Partie suppression d'utilisateurs-------------------------------------------
    function searchDeleteUsers(searchTerm) {

        $.ajax({
            type: "GET",
            url: `/search_delete_user/`,
            data: {
                search_term: searchTerm,
            },
            success: function(data) {
                $("#delete-user-results").html(
                data.delete_users_search_results_html);
            },
            error: function(error) {
                console.log("Erreur de requête AJAX:", error);
            }
        });
    }

    $("#delete-user-form").submit(function(event) {
        event.preventDefault();
        var searchTerm = $("#delete-user-input").val();
        searchDeleteUsers(searchTerm);
    });

    $("#delete-user-results").on("click", ".delete-user-btn", function() {
        const userId = $(this).data('user-id');

        $.ajax({
            url: `/delete_user/`,
            method: "POST",
            data: {
                user_id: userId,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (data) {
                alert(data.message);
                var searchTerm = $("#delete-user-input").val();
                searchDeleteUsers(searchTerm);
            },
            error: function (error) {
                console.log("Erreur de requête AJAX:", error);
            }
        });
    });
});