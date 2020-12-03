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
    return jsonify({'data': result})


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
        return jsonify({'message': "Description missing"}), 422
    if anzahl == "":
        return jsonify({'message': "Link missing"}), 422
    if bild == "":
        return jsonify({'message': "Image missing"}), 422
    if datenblatt == "":
        return jsonify({'message': "Price missing"}), 422
    if library == "":
        return jsonify({'message': "Number missing"}), 422

    try:
        int(anzahl)
    except ValueError:
        return jsonify({'message': "Number is no integer"}), 422

    db = get_db()
    cursor = db.cursor(prepared=True)
    cursor.execute('SELECT * FROM devices WHERE bezeichnung = ?', (bezeichnung, ))
    result = cursor.fetchall()

    if len(result) == 0:
        cursor.execute('INSERT INTO devices (bezeichnung, anzahl, bild, datenblatt, library) '
                       'VALUES (%s, %s, %s, %s, %s)', (bezeichnung, anzahl, bild, datenblatt, library))
        device_id = cursor.lastrowid
        db.commit()

        return jsonify({'message': "Successfully added id=" + str(device_id)})
    else:
        return jsonify({'message': "Already in list"}), 422


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
        return jsonify({'message': "Description missing"}), 422
    if anzahl == "":
        return jsonify({'message': "Link missing"}), 422
    if bild == "":
        return jsonify({'message': "Image missing"}), 422
    if datenblatt == "":
        return jsonify({'message': "Price missing"}), 422
    if library == "":
        return jsonify({'message': "Number missing"}), 422

    try:
        int(anzahl)
    except ValueError:
        return jsonify({'message': "Number is no integer"}), 422

    db = get_db()
    cursor = db.cursor(prepared=True)
    cursor.execute('UPDATE devices SET bezeichnung = %s, anzahl = %s, bild = %s, datenblatt = %s, library = %s '
                   'WHERE id = %s', (bezeichnung, anzahl, bild, datenblatt, library, device_id))
    db.commit()
    return jsonify({'message': "Successfully updated id=" + str(device_id)})


@dev.route('/<int:device_id>', methods=['DELETE'])
@login_required
def delete_device(device_id):
    db = get_db()
    cursor = db.cursor(prepared=True)
    cursor.execute('DELETE FROM devices WHERE id = %s', (device_id,))
    db.commit()
    return jsonify({'message': "Successfully removed id=" + str(device_id)})
