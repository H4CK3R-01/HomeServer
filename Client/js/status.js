$(function () {
    httpGetAsync("http://localhost:5000/api/v1/resources/status/all", "", updateStatus);
});


function updateStatus(data) {
    data = JSON.parse(data);
    $.each(data['data'], (key) => {
        if($("#" + key).length !== 0) {
            if(data['data'][key]['open']) {
                $("#" + key + " > .card-header > .status").removeClass().addClass("status running").text("RUNNING");
            } else {
                $("#" + key + " > .card-header > .status").removeClass().addClass("status stopped").text("STOPPED");
            }

            if (data['data'][key].hasOwnProperty('user')) {
                $("#" + key + " > .card-footer").empty();
                $("#" + key + " > .card-footer").append(`<span>Benutzer: <b>` + data['data'][key]['user'] + `</b></span><br><span>Passwort: <b>` + data['data'][key]['password'] + `</b></span>`);
            }
        }
    });
}