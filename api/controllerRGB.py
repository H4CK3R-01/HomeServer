import json

import mysql.connector
import requests
from flask import jsonify, Blueprint, request

from auth import basicAuth

rgb = Blueprint('rgb', __name__)
last_colors = {}


@rgb.route('/api/v1/resources/rgb/color', methods=['GET'])
def get_color():
    result = execute_sql("SELECT r, g, b, led_id FROM farben_luefter")
    return jsonify({'status': 200, 'data': result})


@rgb.route('/api/v1/resources/rgb/color', methods=['POST'])
@basicAuth.login_required
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
        mydb = mysql.connector.connect(
            host="server.fritz.box",
            user="root",
            passwd="Admin!123",
            database="mydb"
        )
        cursor = mydb.cursor(prepared=True)
        if prepare_sql("SELECT COUNT(1) FROM farben_luefter WHERE led_id = %s", (key,))[0][0] == 1:
            cursor.execute("UPDATE farben_luefter SET r = %s, g = %s, b = %s WHERE led_id = %s", (r, g, b, key))
        else:
            cursor.execute("INSERT INTO farben_luefter (r, g, b, led_id) VALUES (%s, %s, %s, %s)", (r, g, b, key))
        mydb.commit()

        hex_color = '%02x%02x%02x' % (r, g, b)
        colors.append(int(hex_color, 16))

    url = 'http://192.168.178.177'
    x = requests.post(url, data=json.dumps(colors))
    if x.status_code == 200:
        return jsonify({'status': 200})
    else:
        return jsonify({'status': 500})


def execute_sql(sql):
    mydb = mysql.connector.connect(
        host="server.fritz.box",
        user="root",
        passwd="Admin!123",
        database="mydb"
    )
    cursor = mydb.cursor()
    cursor.execute(sql)
    return cursor.fetchall()


def prepare_sql(sql, params):
    mydb = mysql.connector.connect(
        host="server.fritz.box",
        user="root",
        passwd="Admin!123",
        database="mydb"
    )
    cursor = mydb.cursor(prepared=True)
    cursor.execute(sql, params)
    try:
        return cursor.fetchall()
    except mysql.connector.errors.InterfaceError:
        pass
