// Get lists
$(function () {
    httpGetAsync("http://localhost:5000/api/v1/resources/bought/all", "", showBought);

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

// Check all button
$(document).on('click', '#check_all', function() {
    $("#bought").children("tr").each(function () {
        this.firstChild.firstChild.checked = $("#check_all").prop("checked");
    })
    calc();
});

$(document).on('click', 'input[type="checkbox"]', function() {
    calc();
});

$(document).on('click', '#save', function() {
    const data = {};
    data['beschreibung'] = $("#beschreibung").val();
    data['link'] = $("#link").val();
    data['bild'] = $("#bild").val();
    data['anzahl'] = $("#anzahl").val();
    data['preis'] = $("#preis").val();

    httpPostAsync("http://localhost:5000/api/v1/resources/bought", data, add_result);
});

$(document).on('click', '#reset', function() {
    $("#add_form").children("input").each(function ()  {
        $(this).val("");
    });
});

// Calculate price
function calc() {
    let preis_einzeln = 0
    let preis_anzahl = 0
    $("#bought").children("tr").each(function () {
        let preis = $(this).find("input").val();
        let anzahl = $(this).find("td")[4].innerText;

        if($(this).find("input").prop("checked")) {
            preis_einzeln = preis_einzeln + preis * 1;
            preis_anzahl = preis_anzahl + anzahl * preis;
        }
    });
    $("#preis_gesamt_eins").text(preis_einzeln.toFixed(2) + " €");
    $("#preis_gesamt_anzahl").text(preis_anzahl.toFixed(2) + " €");
}


function showBought(data) {
    $("#bought").empty();

    if (isJson(data)) {
        data = JSON.parse(data);

        $.each(data['data'], (key) => {
            let wish = data['data'][key];
            let id = wish[0];
            let desc = wish[1];
            let img = wish[2]
            let anzahl = wish[3];
            let preis = wish[4];
            let link = wish[5];
            let jahr = wish[6];
            let host;
            try {
                host = new URL(link).host;
            } catch (TypeError) {
                host = "";
            }

            $("#bought").append(generate_table_row(id, preis, img, desc, host, anzahl, link, jahr));
        });
    } else {
        $("#notification_area").append('<div class="alert alert-danger" role="alert">Laden der Daten nicht möglich!</div>');
    }
}

function generate_table_row(id, preis, img, desc, host, anzahl, link, jahr) {
    return  "<tr id='row_" + id + "'>" +
                "<td>" +
                    "<input type='checkbox' value='" + preis + "'>" +
                "</td>" +
                "<td>" + id + "</td>" +
                "<td>" +
                    "<img class='img-fluid' alt='product-image' src=" + img + ">" +
                "</td>" +
                "<td>" + desc + "<br><a href=" + link + " target='_blank'>" + host + "</a></td>" +
                "<td>" + anzahl + "</td>" +
                "<td>" + (preis *  1).toFixed(2) + " €</td>" +
                "<td>" + (preis * anzahl).toFixed(2) + " €</td>" +
                "<td>" + jahr + "</td>" +
            "</tr>";
}

function add_result(data) {
    console.log(data)
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
            let jahr = 2020;

            $("#bought").append(generate_table_row(id, preis, img, desc, host, anzahl, jahr));
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