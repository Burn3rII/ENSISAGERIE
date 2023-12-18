window.onload = function() {
    var theme = localStorage.getItem('theme');
    switch (theme) {
        case 'dark-theme':
            $(document.body).toggleClass("dark-theme");
            break;
        default:
            localStorage.setItem("theme","light-theme")
    }
}

$("#theme-switch").click(function() {
    var theme = localStorage.getItem('theme');
    $(document.body).toggleClass("dark-theme");
    switch (theme) {
        case 'dark-theme':
            localStorage.setItem("theme","light-theme")
            break;
        case 'light-theme':
            localStorage.setItem("theme","dark-theme")
            break;
    }
})
