window.onload = function() {
    const toggleButton = document.getElementById('toggle-music-button');
    const audio = document.getElementById('background-music');
    audio.play();
    toggleButton.onclick = function() {
        if (audio.paused) {
            audio.play();
        } else {
            audio.pause();
        }
    };
}