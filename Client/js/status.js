$(function () {
    httpGetAsync("http://127.0.0.1:5000/api/v1/resources/status/all", "", updateStatus);
});


function updateStatus(data) {
    data = JSON.parse(data);
    $.each(data['data'], (key) => {
        if($("#" + key).length !== 0) {
            if(data['data'][key]['data']['open']) {
                $("#" + key + " > .card-header > .status").removeClass().addClass("status running").text("running")
            } else {
                $("#" + key + " > .card-header > .status").removeClass().addClass("status stopped").text("stopped")
            }
        }
    });
}