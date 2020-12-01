// Get lists
$(function () {
    httpGetAsync('/api/v1/resources/wish/lists', "", loadLists);

    // Tabs
    let url = document.location.toString();
    if (url.match('#')) {
        $('.nav-tabs a[href="#' + url.split('#')[1] + '"]').tab('show');
    }
});

// Tabs
$(document).on('shown.bs.tab', '.nav-tabs a', function (e) {
    window.location.hash = e.target.hash;
})

// Select other list
$(document).on('change', '#list', function () {
    $("#wish").empty();
    $("#wish_edit").empty();

    $("#wish").append('<tr><td colspan=\"7\"><div class=\"d-flex justify-content-center\"><div class=\"spinner-border\" role=\"status\"><span class=\"sr-only\">Loading...</span></div></div></td></tr>');
    $("#wish_edit").append('<div class="card"><div class="card-body"><div class="d-flex justify-content-center"><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div></div></div>');

    // Clear price and check-all button
    $('#check_all').prop('checked', false);
    $('#preis_gesamt_anzahl').text("");
    $('#preis_gesamt_eins').text("");

    httpGetAsync('/api/v1/resources/wish/list/' + this.value, "", showWish);
    setGetParameter("list", this.value);
});

// Check all button
$(document).on('click', '#check_all', function () {
    $("#wish").children("tr").each(function () {
        this.firstChild.firstChild.checked = $("#check_all").prop("checked");
    })
    calc();
});

$(document).on('click', 'input[type="checkbox"]', function () {
    calc();
});

$(document).on('click', '#save', function () {
    const data = {};
    data['beschreibung'] = $("#beschreibung").val();
    data['link'] = $("#link").val();
    data['bild'] = $("#bild").val();
    data['anzahl'] = $("#anzahl").val();
    data['preis'] = $("#preis").val();

    httpPostAsync("/api/v1/resources/wish/" + $('#list').val(), data, add_result);
});

$(document).on('click', '#reset', function () {
    $("#add_form").children("input").each(function () {
        $(this).val("");
    });
});

$(document).on('click', '.save', function () {
    let id = this.id.substring(5);
    const data = {};
    data['beschreibung'] = $("#beschreibung_" + id).val();
    data['link'] = $("#link_" + id).val();
    data['bild'] = $("#bild_" + id).val();
    data['anzahl'] = $("#anzahl_" + id).val();
    data['preis'] = $("#preis_" + id).val();
    data['liste'] = $("#liste_" + id).val();
    httpPostAsync("/api/v1/resources/wish/" + id, data, update_result);
});

// Reset input
$(document).on('click', '.reset', function () {
    let id = this.id.substring(6);
    $("#card_" + id).find("input").each(function () {
        $(this).val($(this).attr('placeholder'));
    });
});

// Delete wish
$(document).on('click', '.delete', function () {
    let id = this.id.substring(7);
    httpDeleteAsync("/api/v1/resources/wish/" + id, "", delete_result);
});


// Add new list
$(document).on('change', 'select', function () {
    if ($(this).val() === "new") {
        $('#add_list').modal('show')
    }
});

$(document).on('click', '#add_list_save', function () {
    let list = $("#new_list").val();
    $("[id^=liste_]").each(function () {
        $('<option value="' + list + '">' + list.capitalize() + '</option>').insertBefore('#' + this.id + ' > option:last');
    })
    $("#list").append('<option value="' + list + '">' + list.capitalize() + '</option>');

    $("#add_list").modal('hide');
});

// Calculate price
function calc() {
    let preis_einzeln = 0
    let preis_anzahl = 0
    $("#wish").children("tr").each(function () {
        let preis = $(this).find("input").val();
        let anzahl = $(this).find("td")[4].innerText;

        if ($(this).find("input").prop("checked")) {
            preis_einzeln = preis_einzeln + preis * 1;
            preis_anzahl = preis_anzahl + anzahl * preis;
        }
    });
    $("#preis_gesamt_eins").text(preis_einzeln.toFixed(2) + " €");
    $("#preis_gesamt_anzahl").text(preis_anzahl.toFixed(2) + " €");
}


function loadLists(data) {
    if (isJson(data)) {
        const lists = JSON.parse(data);
        const $select = $('#list');
        $.each(lists['data'], function (key) {
            $select.append('<option value="' + key + '">' + lists['data'][key] + '</option>');
        });

        let get = findGetParameter("list");
        if (get == null) {
            $select.val("wunschliste");
        } else {
            if (selectHasValue("list", get)) $select.val(get);
            else $select.val("wunschliste");
        }

        httpGetAsync('/api/v1/resources/wish/list/' + $select.val(), "", showWish);
    } else {
        $("#notification_area").append('<div class="alert alert-danger" role="alert">Laden der Daten nicht möglich!</div>');
    }
}


function showWish(data) {
    $("#wish").empty();
    $("#wish_edit").empty();

    if (isJson(data)) {
        data = JSON.parse(data);
        $.each(data['data'], (key) => {
            let wish = data['data'][key];
            let id = wish[0];
            let desc = wish[1];
            let link = wish[2];
            let host;
            try {
                host = new URL(link).host;
            } catch (TypeError) {
                host = "";
            }
            let anzahl = wish[4];
            let img = wish[5];
            let preis = wish[6];
            let wichtigkeit = wish[7];
            let liste = wish[8];

            $("#wish").append(generate_table_row(id, preis, wichtigkeit, img, desc, host, anzahl, link));
            $("#wish_edit").append(generate_edit_view(id, desc, img, link, anzahl, preis, liste))

            $('#list > option').each(function () {
                $("#liste_" + id).append('<option value="' + this.value + '">' + this.text + '</option>');
            });
            $("#liste_" + id).append('<option value="new" class="new">Add new list</option>');
            $("#liste_" + id).val(liste);
        });
    } else {
        $("#notification_area").append('<div class="alert alert-danger" role="alert">Laden der Daten nicht möglich!</div>');
    }
}

function generate_table_row(id, preis, wichtigkeit, img, desc, host, anzahl, link) {
    return "<tr id='row_" + id + "'>" +
        "<td>" +
        "<input type='checkbox' value='" + preis + "'>" +
        "</td>" +
        "<td>" + wichtigkeit + "</td>" +
        "<td>" +
        "<img class='img-fluid' alt='product-image' src=" + img + ">" +
        "</td>" +
        "<td>" + desc + "<br><a href=" + link + " target='_blank'>" + host + "</a></td>" +
        "<td>" + anzahl + "</td>" +
        "<td>" + (preis * 1).toFixed(2) + " €</td>" +
        "<td>" + (preis * anzahl).toFixed(2) + " €</td>" +
        "</tr>"
}

function generate_edit_view(id, desc, img, link, anzahl, preis, liste) {
    return '<div class="card" id="card_' + id + '">' +
        '<div class="card-header"><input type="text" class="form-control form-control-sm" placeholder="' + desc + '" name="beschreibung" id="beschreibung_' + id + '" value="' + desc + '" autocomplete="off"></div>' +
        '<div class="card-body">' +
        '<div class="row">' +
        '<div class="col-md-3">' +
        '<img class="img-fluid" alt="product-image" src="' + img + '"/>' +
        '</div>' +
        '<div class="col-md-9">' +
        '<div class="form-group">' +
        '<label for="link">Link:</label>' +
        '<input type="text" class="form-control form-control-sm" placeholder="' + link + '" name="link" id="link_' + id + '" value="' + link + '" autocomplete="off">' +
        '<label for="bild">Bild:</label>' +
        '<input type="text" class="form-control form-control-sm" placeholder="' + img + '" name="bild" id="bild_' + id + '" value="' + img + '" autocomplete="off">' +
        '<label for="anzahl">Anzahl:</label>' +
        '<input type="text" class="form-control form-control-sm" placeholder="' + anzahl + '" name="anzahl" id="anzahl_' + id + '" value="' + anzahl + '" autocomplete="off">' +
        '<label for="preis">Preis:</label>' +
        '<input type="text" class="form-control form-control-sm" placeholder="' + preis + '" name="preis" id="preis_' + id + '" value="' + preis + '" autocomplete="off">' +
        '<label for="liste">Liste:</label>' +
        '<input type="hidden" id="liste_before_' + id + '" value="' + liste + '">' +
        '<select class="form-control form-control-sm" name="liste" id="liste_' + id + '"></select>' +
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

function delete_result(data) {
    if (isJson(data)) {
        data = JSON.parse(data)
        if (data['status'] === 200) {
            $("#notification_area").append('<div class="alert alert-success" role="alert">Erfolgreich gelöscht!</div>')
            let id = data['message'].match(/id=(?<id>\d*)/gm)[0].substring(3);
            $("#card_" + id).remove();
            $("#row_" + id).remove();
        } else {
            $("#notification_area").append('<div class="alert alert-danger" role="alert">' + data['message'] + '</div>');
        }
    } else {
        if (data === "Unauthorized Access") {
            $("#notification_area").append('<div class="alert alert-danger" role="alert">Bitte zuerst anmelden!</div>')
        } else {
            $("#notification_area").append('<div class="alert alert-danger" role="alert">' + data + '</div>');
        }
    }
}

function update_result(data) {
    if (isJson(data)) {
        data = JSON.parse(data)
        if (data['status'] === 200) {
            $("#notification_area").append('<div class="alert alert-success" role="alert">Erfolgreich geändert!</div>');
            let id = data['message'].match(/id=(?<id>\d*)/gm)[0].substring(3);
            if ($("#liste_before_" + id).val() !== $("#liste_" + id).val()) {
                $("#card_" + id).remove();
                $("#row_" + id).remove();
            } else {
                $("#card_" + id).find("input").each(function () {
                    $(this).attr('placeholder', $(this).val());
                });

                let desc = $("#beschreibung_" + id).val();
                let link = $("#link_" + id).val();
                let host;
                try {
                    host = new URL(link).host;
                } catch (TypeError) {
                    host = "";
                }
                let anzahl = $("#anzahl_" + id).val();
                let img = $("#bild_" + id).val();
                let preis = $("#preis_" + id).val();
                let wichtigkeit = 0

                $("#row_" + id).replaceWith(generate_table_row(id, preis, wichtigkeit, img, desc, host, anzahl, link));
            }
        } else {
            $("#notification_area").append('<div class="alert alert-danger" role="alert">' + data['message'] + '</div>');
        }
    } else {
        if (data === "Unauthorized Access") {
            $("#notification_area").append('<div class="alert alert-danger" role="alert">Bitte zuerst anmelden!</div>')
        } else {
            $("#notification_area").append('<div class="alert alert-danger" role="alert">' + data + '</div>');
        }
    }
}


function add_result(data) {
    if (isJson(data)) {
        data = JSON.parse(data)
        if (data['status'] === 200) {
            $("#notification_area").append('<div class="alert alert-success" role="alert">Erfolgreich hinzugefügt!</div>')
            let id = data['message'].match(/id=(?<id>\d*)/gm)[0].substring(3);
            let desc = $("#beschreibung").val();
            let link = $("#link").val();
            let host;
            try {
                host = new URL(link).host;
            } catch (TypeError) {
                host = "";
            }
            let anzahl = $("#anzahl").val();
            let img = $("#bild").val();
            let preis = $("#preis").val();
            let wichtigkeit = 0
            let liste = $("#list").val();

            $(generate_table_row(id, preis, wichtigkeit, img, desc, host, anzahl)).insertBefore('table > tbody > tr:first');
            $(generate_edit_view(id, desc, img, link, anzahl, preis, liste)).insertBefore('#wish_edit > .card:first');
            $('#list > option').each(function () {
                $("#liste_" + id).append('<option value="' + this.value + '">' + this.text + '</option>');
            });
            $("#liste_" + id).append('<option value="new" class="new">Add new list</option>');
            $("#liste_" + id).val(liste);

            $("#reset").trigger("click");
        } else {
            $("#notification_area").append('<div class="alert alert-danger" role="alert">' + data['message'] + '</div>');
        }
    } else {
        if (data === "Unauthorized Access") {
            $("#notification_area").append('<div class="alert alert-danger" role="alert">Bitte zuerst anmelden!</div>')
        } else {
            $("#notification_area").append('<div class="alert alert-danger" role="alert">' + data + '</div>');
        }
    }
}