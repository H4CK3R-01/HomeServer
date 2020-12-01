import json
import socket

import requests
from flask import jsonify, Blueprint, request

from app.auth import login_required
from app.db import get_db

rgb = Blueprint('rgb', __name__, url_prefix='/api/v1/resources/rgb')
last_colors = {}


@rgb.route('/color', methods=['GET'])
def get_color():
    db = get_db()
    cursor = db.cursor(prepared=True)
    cursor.execute('SELECT r, g, b, led_id FROM farben_luefter')
    result = cursor.fetchall()
    return jsonify({'status': 200, 'data': result})


@rgb.route('/color', methods=['POST'])
@login_required
def set_color():
    data = json.loads(request.get_data().decode("ascii"))

    global last_colors
    last_colors = data

    colors = []
    for key, value in data.items():
        print(data)
        r = int(value["color"][1:3], 16)
        g = int(value["color"][3:5], 16)
        b = int(value["color"][5:7], 16)

        db = get_db()
        cursor = db.cursor(prepared=True)
        cursor.execute('SELECT * FROM farben_luefter WHERE led_id = ?', (key,))
        result = cursor.fetchall()
        if len(result) == 0:
            cursor.execute('UPDATE farben_luefter SET r = ?, g = ?, b = ? WHERE led_id = ?', (r, g, b, key))
        else:
            cursor.execute('INSERT INTO farben_luefter (r, g, b, led_id) VALUES (?, ?, ?, ?)', (r, g, b, key))
        db.commit()

        hex_color = '%02x%02x%02x' % (r, g, b)
        colors.append(int(hex_color, 16))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(("192.168.178.177", 80))
    if result == 0:
        url = 'http://192.168.178.177'
        x = requests.post(url, data=json.dumps(colors))
        if x.status_code == 200:
            return jsonify({'status': 200})
        else:
            return jsonify({'status': 500})
    else:
        return jsonify({'status': 500, 'message': 'No connection to arduino'})
