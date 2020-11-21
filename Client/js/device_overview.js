$(function () {
    httpGetAsync('http://ubuntu.fritz.box:9005ubuntu.fritz.box:9005ubuntu.fritz.box:9005ubuntu.fritz.box:9005/api/v1/resources/device', "", showDevices);

    // Tabs
    let url = document.location.toString();
    if (url.match('#')) {
        $('.nav-tabs a[href="#' + url.split('#')[1] + '"]').tab('show');
    }
});

// Tabs
$(document).on('shown.bs.tab', '.nav-tabs a', function(e) {
    window.location.hash = e.target.hash;
})

$(document).on('click', '#save', function() {
    const data = {};
    data['bezeichnung'] = $("#bezeichnung").val();
    data['anzahl'] = $("#anzahl").val();
    data['bild'] = $("#bild").val();
    data['datenblatt'] = $("#datenblatt").val();
    data['library'] = $("#library").val();

    httpPostAsync("http://ubuntu.fritz.box:9005ubuntu.fritz.box:9005ubuntu.fritz.box:9005ubuntu.fritz.box:9005/api/v1/resources/device", data, add_result);
});

$(document).on('click', '#reset', function() {
    $("#add_form").children("input").each(function ()  {
        $(this).val("");
    });
});

$(document).on('click', '.save', function () {
    let id = this.id.substring(5);
    const data = {};
    data['bezeichnung'] = $("#bezeichnung_" + id).val();
    data['anzahl'] = $("#anzahl_" + id).val();
    data['bild'] = $("#bild_" + id).val();
    data['datenblatt'] = $("#datenblatt_" + id).val();
    data['library'] = $("#library_" + id).val();
    httpPutAsync("http://ubuntu.fritz.box:9005/api/v1/resources/device/" + id, data, update_result);
});

// Reset input
$(document).on('click', '.reset', function () {
    let id = this.id.substring(6);
    $("#card_" + id).find("input").each(function ()  {
        $(this).val($(this).attr('placeholder'));
    });
});

// Delete device
$(document).on('click', '.delete', function () {
    let id = this.id.substring(7);
    httpDeleteAsync("http://ubuntu.fritz.box:9005/api/v1/resources/device/" + id, "", delete_result);
});

function showDevices(data) {
    $("#devices").empty();
    $("#devices_edit").empty();

    data = JSON.parse(data);
    $.each(data['data'], (key) => {
        let device = data['data'][key];
        let id = device[0];
        let bezeichnung = device[1];
        let anzahl = device[2];
        let bild = device[3];
        let datenblatt = device[4];
        let datenblatt_host;
        try {
            datenblatt_host = new URL(datenblatt).host;
        } catch (TypeError) {
            datenblatt_host = "";
        }
        let library = device[5];
        let library_host;
        try {
            library_host = new URL(library).host;
        } catch (TypeError) {
            library_host = "";
        }

        $("#devices").append(generate_table_row(id, bezeichnung, anzahl, bild, datenblatt, datenblatt_host, library, library_host));

        $("#devices_edit").append(generate_edit_view(id, bezeichnung, anzahl, bild, datenblatt, library))
    });
}

function generate_table_row(id, bezeichnung, anzahl, img, datenblatt, datenblatt_host, library, library_host) {
    return  "<tr id='row_" + id + "'>" +
                "<td>" + id + "</td>" +
                "<td>" +
                    "<img class='img-fluid' alt='product-image' src=" + img + ">" +
                "</td>" +
                "<td>" + bezeichnung + "<br><a href=" + datenblatt + " target='_blank'>" + datenblatt_host + "</a><br><a href=" + library + " target='_blank'>" + library_host + "</a></td>" +
                "<td>" + anzahl + "</td>" +
            "</tr>"
}

function generate_edit_view(id, bezeichnung, anzahl, bild, datenblatt, library) {
    return  '<div class="card" id="card_' + id + '">' +
                '<div class="card-header"><input type="text" class="form-control form-control-sm" placeholder="' + bezeichnung + '" name="bezeichnung" id="bezeichnung_' + id + '" value="' + bezeichnung + '" autocomplete="off"></div>' +
                    '<div class="card-body">' +
                        '<div class="row">' +
                            '<div class="col-md-3">' +
                                '<img class="img-fluid" alt="product-image" src="' + bild + '"/>' +
                            '</div>' +
                            '<div class="col-md-9">' +
                                '<div class="form-group">' +
                                    '<label for="anzahl">Anzahl:</label>' +
                                    '<input type="text" class="form-control form-control-sm" placeholder="' + anzahl + '" name="anzahl" id="anzahl_' + id + '" value="' + anzahl + '" autocomplete="off">' +
                                    '<label for="bild">Bild:</label>' +
                                    '<input type="text" class="form-control form-control-sm" placeholder="' + bild + '" name="bild" id="bild_' + id + '" value="' + bild + '" autocomplete="off">' +
                                    '<label for="datenblatt">Datenblatt:</label>' +
                                    '<input type="text" class="form-control form-control-sm" placeholder="' + datenblatt + '" name="datenblatt" id="datenblatt_' + id + '" value="' + datenblatt + '" autocomplete="off">' +
                                    '<label for="library">Library:</label>' +
                                    '<input type="text" class="form-control form-control-sm" placeholder="' + library + '" name="library" id="library_' + id + '" value="' + library + '" autocomplete="off">' +
                                '</div>' +
                            '</div>' +
                        '</div>' +
                    '</div>' +
                    '<div class="card-footer">' +
                        '<button class="btn btn-primary save" id="save_' + id + '">Speichern</button>' +
                        '<button class="btn btn-secondary reset" id="reset_' + id + '">Zurücksetzen</button>' +
                        '<button class="btn btn-danger delete" id="delete_' + id + '">Löschen</button>' +
                    '</div>' +
                '</div>' +
            '</div>'
}

function delete_result(message) {
    let data = JSON.parse(message)
    if(data['status'] === 200) {
        let id = data['message'].match(/id=(?<id>\d*)/gm)[0].substring(3);
        $("#card_" + id).remove();
        $("#row_" + id).remove();
    } else {
        console.error(data);
    }
}

function update_result(message) {
    let data = JSON.parse(message)
    if(data['status'] === 200) {
        let id = data['message'].match(/id=(?<id>\d*)/gm)[0].substring(3);
        if($("#liste_before_" + id).val() !== $("#liste_" + id).val()) {
            $("#card_" + id).remove();
            $("#row_" + id).remove();
        } else {
            $("#card_" + id).find("input").each(function ()  {
                $(this).attr('placeholder', $(this).val());
            });

            let bezeichnung = $("#bezeichnung_" + id).val();
            let anzahl = $("#anzahl_" + id).val();
            let bild = $("#bild_" + id).val();
            let datenblatt = $("#datenblatt_" + id).val();
            let datenblatt_host;
            try {
                datenblatt_host = new URL(datenblatt).host;
            } catch (TypeError) {
                datenblatt_host = "";
            }
            let library = $("#library_" + id).val();
            let library_host;
            try {
                library_host = new URL(library).host;
            } catch (TypeError) {
                library_host = "";
            }

            $("#row_" + id).replaceWith(generate_table_row(id, bezeichnung, anzahl, bild, datenblatt, datenblatt_host, library, library_host));
        }
    } else {
        console.error(data)
    }
}

function add_result(message) {
    let data = JSON.parse(message)
    if(data['status'] === 200) {
        let id = data['message'].match(/id=(?<id>\d*)/gm)[0].substring(3);
        let bezeichnung = $("#bezeichnung").val();
        let anzahl = $("#anzahl").val();
        let bild = $("#bild").val();
        let datenblatt = $("#datenblatt").val();
        let datenblatt_host;
        try {
            datenblatt_host = new URL(datenblatt).host;
        } catch (TypeError) {
            datenblatt_host = "";
        }
        let library = $("#library").val();
        let library_host;
        try {
            library_host = new URL(library).host;
        } catch (TypeError) {
            library_host = "";
        }
        $('#devices').append(generate_table_row(id, bezeichnung, anzahl, bild, datenblatt, datenblatt_host, library, library_host));
        $('#devices_edit').append(generate_edit_view(id, bezeichnung, anzahl, bild, datenblatt, library));

        $("#reset").trigger("click");
    } else {
        console.error(data)
    }
}