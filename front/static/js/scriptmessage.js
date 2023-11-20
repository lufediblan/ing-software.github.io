document.addEventListener('DOMContentLoaded', function () {
    var messageElement = document.getElementById("message");
    if (messageElement.innerText.trim() !== '') {
        setTimeout(function () {
            messageElement.style.color = 'transparent'; /* Cambiar a un color transparente */
        }, 3000);
    }
});