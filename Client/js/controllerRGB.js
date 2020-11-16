function Circle(x, y, r, color) {
    this.x = x;
    this.y = y;
    this.r = r;
    this.color = color;
}

$(function () {
    httpGetAsync("http://127.0.0.1:5000/api/v1/resources/rgb/color", "", generateCircles);
})

function generateCircles(data) {
    data = JSON.parse(data);

    let canvas = document.getElementById('luefter');
    let ctx = canvas.getContext('2d');
    canvas.width = 400
    canvas.height = 400
    ctx.translate(canvas.width/2,canvas.height/2);
    ctx.lineWidth = 2

    let circles = {}
    for(let i = 0; i < 20; i++) {
        let r = componentToHex(data.data[i][0]);
        let g = componentToHex(data.data[i][1]);
        let b = componentToHex(data.data[i][2]);
        let color = r + g + b;
        circles[i] = new Circle(Math.cos(18*i * (Math.PI / 180)) * 170, Math.sin(18*i * (Math.PI / 180)) * 170, 15, "#" + color);
    }

    $.each(circles, function( key, value ) {
        ctx.fillStyle = value.color;
        ctx.beginPath();
        ctx.arc(value.x, value.y, value.r, 0, Math.PI * 2, true);
        ctx.closePath();
        ctx.fill();
    });

    let thumbImg = document.createElement('img');
    thumbImg.onload = function() {
        ctx.lineWidth = 5
        ctx.save();
        ctx.beginPath();
        ctx.arc(0, 0, 130, 0, Math.PI * 2, true);
        ctx.closePath();
        ctx.stroke();

        ctx.drawImage(thumbImg, -100, -100, 200, 200);
    };

    thumbImg.src = '../img/luefter.png';

    canvas.addEventListener('click', function(e) {
        let xy = getMousePos(canvas, e);
        let x = xy.x - 200;
        let y = xy.y - 200;

        for(let i = 0; i < 20; i++) {
            if(Math.pow(x-(Math.cos(18*i * (Math.PI / 180)) * 170),2)+Math.pow(y-(Math.sin(18*i * (Math.PI / 180)) * 170),2) < Math.pow(15,2)) {
                circles[i].color = document.getElementById("c").value;
                ctx.fillStyle = document.getElementById("c").value
                ctx.beginPath();
                ctx.arc(Math.cos(18*i * (Math.PI / 180)) * 170, Math.sin(18*i * (Math.PI / 180)) * 170, 15, 0, Math.PI * 2, true);
                ctx.closePath();
                ctx.fill();
                httpPostAsync("http://127.0.0.1:5000/api/v1/resources/rgb/color", circles, changeColor)
                // httpPostAsync("http://192.168.178.177", circles, changeColor)
            }
        }
    }, false);
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

function changeColor(data) {
    console.log(data)
}

function componentToHex(c) {
    c = parseInt(c)
    let hex = c.toString(16);
    return hex.length === 1 ? "0" + hex : hex;
}