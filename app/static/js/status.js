$(function () {
    httpGetAsync("/api/v1/resources/status/all", "", update_status_callback);
});


// Callbacks
function update_status_callback(data, status) {
    if (status === 200) { // OK
        data = JSON.parse(data);
        $.each(data['data'], (key) => {
            if ($("#" + key).length !== 0) {
                if (data['data'][key]['open']) {
                    $("#" + key + " > .card-header > .status").removeClass().addClass("status running").text("RUNNING");
                } else {
                    $("#" + key + " > .card-header > .status").removeClass().addClass("status stopped").text("STOPPED");
                }

                if (data['data'][key].hasOwnProperty('user')) {
                    $("#" + key + " > .card-footer").empty().append(`<span>Benutzer: <b>` + data['data'][key]['user'] + `</b></span><br><span>Passwort: <b>` + data['data'][key]['password'] + `</b></span>`);
                }
            }
        });
    } else if (status === 401) { // Authentication required
        data = JSON.parse(data)
        $("#notification_area").append(createNotification('danger', data['message']));
    } else if (status === 422) { // Data missing in request
        data = JSON.parse(data)
        $("#notification_area").append(createNotification('danger', data['message']));
    } else {
        $("#notification_area").append(createNotification('danger', "Unbekannter Fehler"));
    }
}