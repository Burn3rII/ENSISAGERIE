$(document).ready(function() {
    $("#search-form").submit(function(event) {
        event.preventDefault();
        var searchTerm = $("#search-input").val();

        $.ajax({
            type: "GET",
            url: "/rooms/search/",
            data: {
                'search_term': searchTerm,
            },
            success: function(data) {
                $("#search-results").html(data.search_results_html);
            },
            error: function(error) {
                console.log("Erreur de requête AJAX:", error);
            }
        });
    });
});
