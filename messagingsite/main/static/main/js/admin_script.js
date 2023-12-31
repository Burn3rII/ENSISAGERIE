$(document).ready(function() {

// Partie suppression d'utilisateurs-------------------------------------------
    var searchTermDelete;

    function searchDeleteUsers() {

        $.ajax({
            type: "GET",
            url: `/search_delete_user/`,
            data: {
                search_term: searchTermDelete,
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
        searchTermDelete = $("#delete-user-input").val();
        searchDeleteUsers();
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
                searchDeleteUsers();
            },
            error: function (error) {
                console.log("Erreur de requête AJAX:", error);
            }
        });
    });
});