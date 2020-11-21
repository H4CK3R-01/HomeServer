from flask import request, jsonify, Blueprint
from tools import execute_sql, prepare_sql

dev = Blueprint('dev', __name__)


@dev.route('/api/v1/resources/device', methods=['GET'])
def get_devices():
    result = execute_sql("SELECT * FROM devices")
    return jsonify({'status': 200, 'data': result})


@dev.route('/api/v1/resources/device', methods=['POST'])
def add_device():
    data = request.json
    bezeichnung = data['bezeichnung']
    anzahl = data['anzahl']
    bild = data['bild']
    datenblatt = data['datenblatt']
    library = data['library']

    if bezeichnung == "":
        return jsonify({'status': 500, 'message': "Description missing"})
    if anzahl == "":
        return jsonify({'status': 500, 'message': "Link missing"})
    if bild == "":
        return jsonify({'status': 500, 'message': "Image missing"})
    if datenblatt == "":
        return jsonify({'status': 500, 'message': "Price missing"})
    if library == "":
        return jsonify({'status': 500, 'message': "Number missing"})

    try:
        int(anzahl)
    except ValueError:
        return jsonify({'status': 500, 'message': "Number is no integer"})

    # TODO SQL Injection
    result = execute_sql("SELECT * FROM devices WHERE bezeichnung = '" + bezeichnung + "'")

    if len(result) == 0:
        device_id = prepare_sql(
            "INSERT INTO devices (bezeichnung, anzahl, bild, datenblatt, library) "
            "VALUES (%s, %s, %s, %s, %s)",
            (bezeichnung, anzahl, bild, datenblatt, library))

        return jsonify({'status': 200, 'message': "Successfully added id=" + str(device_id)})
    else:
        return jsonify({'status': 500, 'message': "Already in list"})


@dev.route('/api/v1/resources/device/<int:device_id>', methods=['PUT'])
def update_device(device_id):
    data = request.json
    bezeichnung = data['bezeichnung']
    anzahl = data['anzahl']
    bild = data['bild']
    datenblatt = data['datenblatt']
    library = data['library']

    if bezeichnung == "":
        return jsonify({'status': 500, 'message': "Description missing"})
    if anzahl == "":
        return jsonify({'status': 500, 'message': "Link missing"})
    if bild == "":
        return jsonify({'status': 500, 'message': "Image missing"})
    if datenblatt == "":
        return jsonify({'status': 500, 'message': "Price missing"})
    if library == "":
        return jsonify({'status': 500, 'message': "Number missing"})

    try:
        int(anzahl)
    except ValueError:
        return jsonify({'status': 500, 'message': "Number is no integer"})

    prepare_sql("UPDATE devices SET bezeichnung = %s, anzahl = %s, bild = %s, datenblatt = %s, library = %s "
                "WHERE id = %s", (bezeichnung, anzahl, bild, datenblatt, library, device_id))
    return jsonify({'status': 200, 'message': "Successfully updated id=" + str(device_id)})


@dev.route('/api/v1/resources/device/<int:device_id>', methods=['DELETE'])
def delete_device(device_id):
    prepare_sql("DELETE FROM devices WHERE id = %s", (device_id,))
    return jsonify({'status': 200, 'message': "Successfully removed id=" + str(device_id)})
