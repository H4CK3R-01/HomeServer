$(function () {
    if (localStorage.getItem('token') !== null) {
        $("#notification_area").append('<div class="alert alert-success" role="alert">You are already logged in!</div>')
    }
});

$("#submit").on("click", function () {
    httpGetAsyncOnlyLogin("http://localhost:5000/api/v1/resources/auth/token", "", login_callback)
    return false;
});

function httpGetAsyncOnlyLogin(url, data, callback) {
    const xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function () {
        if (this.readyState === 4) {
            callback(xmlHttp.responseText);
        }
    }

    xmlHttp.open("GET", url, true); // true for asynchronous
    xmlHttp.setRequestHeader("Authorization", "Basic " + btoa($("#user").val() + ":" + $("#password").val()));
    xmlHttp.send(null);
}

function login_callback(data) {
    if (data === "Unauthorized Access") {
        $("#notification_area").append('<div class="alert alert-danger" role="alert">Login failed. Please check username and password!</div>')
    } else {
        localStorage.setItem('token', JSON.parse(data)['token']);
        window.location.href = "status.html";
    }
    return false;
}