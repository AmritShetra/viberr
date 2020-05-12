/**
 * Play a selected song on the music player (embedded on base template).
 * @param song      URL of the song (string)
 * @param name      Name of the song (string)
 * @param artist    Artist of the song (string)
 */
function playMusic(song, name, artist) {
    document.getElementById("text").innerText = "You're listening to " + name + " by " + artist;
    const audio = document.getElementById("audio");
    audio.src = song;
    audio.play();
}
