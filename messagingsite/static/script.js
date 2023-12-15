window.onload = function(){
    var theme = localStorage.getItem('theme')
    switch (theme) {
        case 'dark-theme':
            document.body.classList.toggle("dark-theme");
            break;
        default:
            localStorage.setItem("theme","light-theme")
    }
}

$("#theme-switch").click(function(){
    var theme = localStorage.getItem('theme')
    document.body.classList.toggle("dark-theme");
    switch (theme) {
        case 'dark-theme':
            localStorage.setItem("theme","light-theme")
            //theme = localStorage.getItem('theme')
            //console.log(theme)
            break;
        case 'light-theme':
            localStorage.setItem("theme","dark-theme")
            //theme = localStorage.getItem('theme')
            //console.log(theme)
            break;
        //default:
        //    localStorage.setItem("theme","light-theme")
    //document.body.classList.toggle("dark-theme");
    }
})
