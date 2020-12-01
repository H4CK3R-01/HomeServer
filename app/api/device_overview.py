from flask import request, jsonify, Blueprint
from app.auth import login_required
from app.db import get_db

dev = Blueprint('dev', __name__, url_prefix='/api/v1/resources/device')


@dev.route('/', methods=['GET'])
def get_devices():
    db = get_db()
    cursor = db.cursor(prepared=True)
    cursor.execute('SELECT * FROM devices')
    result = cursor.fetchall()
    return jsonify({'status': 200, 'data': result})


@dev.route('/', methods=['POST'])
@login_required
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

    db = get_db()
    cursor = db.cursor(prepared=True)
    cursor.execute('SELECT * FROM devices WHERE bezeichnung = ?', (bezeichnung, ))
    result = cursor.fetchall()

    if len(result) == 0:
        cursor.execute('INSERT INTO devices (bezeichnung, anzahl, bild, datenblatt, library) '
                       'VALUES (%s, %s, %s, %s, %s)', (bezeichnung, anzahl, bild, datenblatt, library))
        device_id = cursor.lastrowid
        db.commit()

        return jsonify({'status': 200, 'message': "Successfully added id=" + str(device_id)})
    else:
        return jsonify({'status': 500, 'message': "Already in list"})


@dev.route('/<int:device_id>', methods=['PUT'])
@login_required
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

    db = get_db()
    cursor = db.cursor(prepared=True)
    cursor.execute('UPDATE devices SET bezeichnung = %s, anzahl = %s, bild = %s, datenblatt = %s, library = %s '
                   'WHERE id = %s', (bezeichnung, anzahl, bild, datenblatt, library, device_id))
    db.commit()
    return jsonify({'status': 200, 'message': "Successfully updated id=" + str(device_id)})


@dev.route('/<int:device_id>', methods=['DELETE'])
@login_required
def delete_device(device_id):
    db = get_db()
    cursor = db.cursor(prepared=True)
    cursor.execute('DELETE FROM devices WHERE id = %s', (device_id,))
    db.commit()
    return jsonify({'status': 200, 'message': "Successfully removed id=" + str(device_id)})
