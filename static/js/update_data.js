function sendRequest() {
    var updateButton = document.getElementById("update_data");

    var lastRequestDate = localStorage.getItem("lastRequestDate");
    var currentDate = new Date().toLocaleDateString();

    if (lastRequestDate === currentDate) {
        console.log("Запрос уже был отправлен сегодня. Повторная отправка не допускается.");
        return;
    }
    else {
        localStorage.setItem("lastRequestDate", currentDate);
    }

    updateButton.disabled = true;

    var xhr = new XMLHttpRequest();

    xhr.open("GET", "/update_data", true);
    xhr.onload = function () {
        if (xhr.status >= 200 && xhr.status < 300) {
            console.log("Запрос успешно отправлен");
        } else {
            console.error("Произошла ошибка при отправке запроса");
        }
    };
    xhr.onerror = function () {
        console.error("Произошла ошибка сети");
        updateButton.disabled = false;
    };
    xhr.send();
}

var updateButton = document.getElementById("update_data");
updateButton.addEventListener("click", sendRequest);

var lastRequestDate = localStorage.getItem("lastRequestDate");
var currentDate = new Date().toLocaleDateString();
if (lastRequestDate === currentDate) {
    updateButton.disabled = true;
}
else {
    updateButton.disabled = false;
}