$(function () {
    httpGetAsync("http://ubuntu.fritz.box:9005/api/v1/resources/status/all", "", updateStatus);
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