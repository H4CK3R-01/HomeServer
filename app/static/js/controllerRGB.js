function Circle(x, y, r, color) {
    this.x = x;
    this.y = y;
    this.r = r;
    this.color = color;
}

let luefter = 6;
let colorPicker;
let circles = {};
$(function () {
    colorPicker = new iro.ColorPicker('#picker', {
        width: 400
    });

    let url = document.location.toString();
    if (url.match('#')) {
        $('.nav-tabs a[href="#' + url.split('#')[1] + '"]').tab('show');
    }

    httpGetAsync("/api/v1/resources/rgb/color", "", generate_circles_callback);
});

function redraw_circles() {
    for(let l = 0; l < luefter; l++) {
        let canvas = document.getElementById('luefter' + l);
        let ctx = canvas.getContext('2d');
        for (let i = l * 20; i < l * 20 + 20; i++) {
            console.log(circles[i].color)
            ctx.fillStyle = circles[i].color;
            ctx.beginPath();
            ctx.arc(circles[i].x, circles[i].y, circles[i].r, 0, Math.PI * 2, true);
            ctx.closePath();
            ctx.fill();
        }
    }
}

function getMousePos(canvas, evt) {
    let rect = canvas.getBoundingClientRect(), // abs. size of element
        scaleX = canvas.width / rect.width,    // relationship bitmap vs. element for X
        scaleY = canvas.height / rect.height;  // relationship bitmap vs. element for Y

    return {
        x: (evt.clientX - rect.left) * scaleX,   // scale mouse coordinates after they have
        y: (evt.clientY - rect.top) * scaleY     // been adjusted to be relative to element
    }
}

function componentToHex(c) {
    c = parseInt(c)
    let hex = c.toString(16);
    return hex.length === 1 ? "0" + hex : hex;
}


// Callbacks
function generate_circles_callback(data, status) {
    if (status === 200) {
        data = JSON.parse(data);

        for(let l = 0; l < luefter; l++) {
            $('#tab-nav').append('<li class="nav-item"><a class="nav-link" data-toggle="tab" id="luefter' + l + '_nav_tab" href="#luefter' + l + '_tab">Lüfter ' + (l + 1) + '</a></li>');
            if(l === 0) $('#luefter' + l + '_nav_tab').addClass('active');

            $('#tab-content').append(
                '<div class="tab-pane" id="luefter' + l + '_tab" role="tabpanel">' +
                    '<canvas id="luefter' + l + '"></canvas>' +
                    '<div class="row" style="margin-bottom: 8px">' +
                        '<div class="col-6"><button class="turn-left form-control btn btn-warning" type="button"><-</button></div>' +
                        '<div class="col-6 text-right"><button class="turn-right form-control btn btn-warning" type="button">-></button></div>' +
                    '</div>' +
                    '<button class="rainbow form-control btn btn-success btn-block" type="button">Regenbogenfarben</button>' +
                    '<button class="all form-control btn btn-secondary btn-block" type="button">Alle LEDs in dieser Farbe</button>' +
                    '<button class="save form-control btn btn-primary btn-block" type="button">Speichern</button>' +
                '</div>'
            );
            if(l === 0) $('#luefter' + l + '_tab').addClass('active');

            let canvas = document.getElementById('luefter' + l);
            let ctx = canvas.getContext('2d');
            canvas.width = 400
            canvas.height = 400
            ctx.translate(canvas.width / 2, canvas.height / 2);
            ctx.lineWidth = 2

            for (let i = l * 20; i < l * 20 + 20; i++) {
                let r = componentToHex(data.data[i][0]);
                let g = componentToHex(data.data[i][1]);
                let b = componentToHex(data.data[i][2]);
                let color = r + g + b;
                circles[i] = new Circle(Math.cos(18 * i * (Math.PI / 180)) * 170, Math.sin(18 * i * (Math.PI / 180)) * 170, 15, "#" + color);
            }

            let thumbImg = document.createElement('img');
            thumbImg.onload = function () {
                ctx.lineWidth = 5
                ctx.save();
                ctx.beginPath();
                ctx.arc(0, 0, 130, 0, Math.PI * 2, true);
                ctx.closePath();
                ctx.stroke();

                ctx.drawImage(thumbImg, -100, -100, 200, 200);
            };

            thumbImg.src = 'static/img/luefter.png';

            canvas.addEventListener('click', function (e) {
                let xy = getMousePos(canvas, e);
                let x = xy.x - 200;
                let y = xy.y - 200;

                for (let i = l * 20; i < l * 20 + 20; i++) {
                    if (Math.pow(x - (Math.cos(18 * i * (Math.PI / 180)) * 170), 2) + Math.pow(y - (Math.sin(18 * i * (Math.PI / 180)) * 170), 2) < Math.pow(15, 2)) {
                        circles[i].color = colorPicker.colors[0].hexString;
                        ctx.fillStyle = circles[i].color;
                        ctx.beginPath();
                        ctx.arc(Math.cos(18 * i * (Math.PI / 180)) * 170, Math.sin(18 * i * (Math.PI / 180)) * 170, 15, 0, Math.PI * 2, true);
                        ctx.closePath();
                        ctx.fill();
                    }
                }
            }, false);
        }
        redraw_circles();

        $('.rainbow').on('click', function () {
            let id  = $(this).parent('div').attr('id').substring(7, 8);
            console.log(id)

            for (let i = id * 20; i < id * 20 + 20; i++) {
                circles[i].color = hslToHex(360 / 20 * i, 100, 50);
            }
            redraw_circles();
        });

        $('.all').on('click', function () {
            let id  = $(this).parent('div').attr('id').substring(7, 8);

            for (let i = id * 20; i < id * 20 + 20; i++) {
                circles[i].color = colorPicker.colors[0].hexString;
            }
            redraw_circles();
        });

        $('.turn-left').on('click', function () {
            let id  = $(this).parent('div').parent('div').parent('div').attr('id').substring(7, 8);

            let tmp = circles[id * 20].color;
            for (let i = id * 20; i < id * 20 + 19; i++) {
                circles[i].color = circles[i + 1].color
            }
            circles[id * 20 + 19].color = tmp;
            redraw_circles();
        });

        $('.turn-right').on('click', function () {
            let id  = $(this).parent('div').parent('div').parent('div').attr('id').substring(7, 8);

            let tmp = circles[id * 20 + 19].color;
            for (let i = id * 20 + 19; i > id * 20; i--) {
                circles[i].color = circles[i - 1].color;
            }
            circles[id * 20].color = tmp;
            redraw_circles();
        });

        $('.save').on('click', function () {
            httpPostAsync('/api/v1/resources/rgb/color', circles, change_color_callback)
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

function change_color_callback(data, status) {
    if (status === 200) { // OK
        data = JSON.parse(data)
        $("#notification_area").append(createNotification('success',data['message']))
    } else if (status === 401) { // Authentication required
        data = JSON.parse(data)
        $("#notification_area").append(createNotification('danger', data['message']));
    } else if (status === 423) { // Data missing in request
        data = JSON.parse(data)
        $("#notification_area").append(createNotification('danger', data['message']));
    } else {
        $("#notification_area").append(createNotification('danger', "Unbekannter Fehler"));
    }
}