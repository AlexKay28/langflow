document.onkeyup = function (e) {
    e = e || window.event;
    if (e.keyCode === 13) {
        document.getElementById("next_button").click()
    }
    return false
}
