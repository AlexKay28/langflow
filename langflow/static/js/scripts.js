document.onkeydown = function (e) {
    e = e || window.event;
    if (e.keyCode === 13 && !e.repeat) {
        document.getElementById("next_button").click()
    }
}
