// Get lists
$(function () {
    httpGetAsync("/api/v1/resources/bought/", "", show_bought_callback);

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

// Check all button
$(document).on('click', '#check_all', function () {
    $("#bought").children("tr").each(function () {
        this.firstChild.firstChild.checked = $("#check_all").prop("checked");
    })
    calculate_price();
});

$(document).on('click', 'input[type="checkbox"]', function () {
    calculate_price();
});

$(document).on('click', '#save', function () {
    const data = {};
    data['beschreibung'] = $("#beschreibung").val();
    data['link'] = $("#link").val();
    data['bild'] = $("#bild").val();
    data['anzahl'] = $("#anzahl").val();
    data['preis'] = $("#preis").val();

    httpPostAsync("/api/v1/resources/bought/", data, add_result_callback);
});

$(document).on('click', '#reset', function () {
    $("#add_form").children("input").each(function () {
        $(this).val("");
    });
});


function calculate_price() {
    let preis_einzeln = 0
    let preis_anzahl = 0
    $("#bought").children("tr").each(function () {
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

function generate_table_row(id, preis, img, desc, host, anzahl, link, jahr) {
    return "<tr id='row_" + id + "'>" +
        "<td>" +
        "<input type='checkbox' value='" + preis + "'>" +
        "</td>" +
        "<td>" + id + "</td>" +
        "<td>" +
        "<img class='img-fluid' alt='product-image' src=" + img + ">" +
        "</td>" +
        "<td>" + desc + "<br><a href=" + link + " target='_blank'>" + host + "</a></td>" +
        "<td>" + anzahl + "</td>" +
        "<td>" + (preis * 1).toFixed(2) + " €</td>" +
        "<td>" + (preis * anzahl).toFixed(2) + " €</td>" +
        "<td>" + jahr + "</td>" +
        "</tr>";
}


// Callbacks
function show_bought_callback(data, status) {
    if (status === 200) { // OK
        data = JSON.parse(data)
        $("#bought").empty();
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

function add_result_callback(data, status) {
    if (status === 200) { // OK
        data = JSON.parse(data)
        $("#notification_area").append(createNotification('success',data['message']))
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
        let jahr = new Date().getFullYear();

        $("#bought").append(generate_table_row(id, preis, img, desc, host, anzahl, jahr));
        $("#reset").trigger("click");
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