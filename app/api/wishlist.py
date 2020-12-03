import json
import os

from flask import request, jsonify, Blueprint

from app.auth import login_required
from app.db import get_db

wish = Blueprint('wish', __name__, url_prefix='/api/v1/resources/wish')
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


@wish.route('/lists', methods=['GET'])
def wish_lists():
    db = get_db()
    cursor = db.cursor(prepared=True)
    cursor.execute('SELECT DISTINCT liste FROM wunschliste')
    result = cursor.fetchall()
    lists_dict = {}
    with open(os.path.join(__location__, '../list.config')) as config:
        data = json.load(config)

    for s in result:
        s = s[0]
        if s in data["wishlist"]:
            lists_dict[s] = data["wishlist"][s]
        else:
            lists_dict[s] = s.capitalize()

    return jsonify({'status': 200, 'data': lists_dict})


@wish.route('/list/<string:wish_list>', methods=['GET'])
def wish_one_list(wish_list):
    db = get_db()
    cursor = db.cursor(prepared=True)
    cursor.execute('SELECT * FROM wunschliste WHERE liste = ? ORDER BY wichtigkeit', (wish_list, ))
    result = cursor.fetchall()
    return jsonify({'data': result})


@wish.route('/<string:wish_list>', methods=['POST'])
@login_required
def add_wish(wish_list):
    data = request.json

    beschreibung = data['beschreibung']
    link = data['link']
    bild = data['bild']
    preis = data['preis']
    anzahl = data['anzahl']

    if beschreibung == "":
        return jsonify({'message': "Description missing"}), 500
    if link == "":
        return jsonify({'message': "Link missing"}), 500
    if bild == "":
        return jsonify({'message': "Image missing"}), 500
    if preis == "":
        return jsonify({'message': "Price missing"}), 500
    if anzahl == "":
        return jsonify({'message': "Number missing"}), 500

    try:
        float(preis)
    except ValueError:
        return jsonify({'message': "Price is no number"}), 500

    try:
        int(anzahl)
    except ValueError:
        return jsonify({'message': "Number is no integer"}), 500

    db = get_db()
    cursor = db.cursor(prepared=True)
    cursor.execute('SELECT * FROM wunschliste WHERE link = ? AND liste = ?', (link, wish_list))
    result = cursor.fetchall()

    if len(result) == 0:
        cursor.execute('INSERT INTO wunschliste (beschreibung, link, anzahl, bild, preis, liste) '
                       'VALUES (?, ?, ?, ?, ?, ?)', (beschreibung, link, anzahl, bild, preis, wish_list))
        db.commit()
        wish_id = cursor.lastrowid
        return jsonify({'message': "Successfully added id=" + str(wish_id)})
    else:
        return jsonify({'message': "Already in list"}), 500


@wish.route('/<int:wish_id>', methods=['POST'])
@login_required
def update_wish(wish_id):
    data = request.json
    beschreibung = data['beschreibung']
    link = data['link']
    bild = data['bild']
    preis = data['preis']
    anzahl = data['anzahl']
    liste = data['liste']

    if beschreibung == "":
        return jsonify({'message': "Description missing"}), 500
    if link == "":
        return jsonify({'message': "Link missing"}), 500
    if bild == "":
        return jsonify({'message': "Image missing"}), 500
    if preis == "":
        return jsonify({'message': "Price missing"}), 500
    if anzahl == "":
        return jsonify({'message': "Number missing"}), 500
    if liste == "":
        return jsonify({'message': "List missing"}), 500

    try:
        float(preis)
    except ValueError:
        return jsonify({'message': "Price is no number"}), 500

    try:
        int(anzahl)
    except ValueError:
        return jsonify({'message': "Number is no integer"}), 500

    db = get_db()
    cursor = db.cursor(prepared=True)
    cursor.execute('UPDATE wunschliste SET beschreibung = ?, link = ?, anzahl = ?, bild = ?, preis = ?, liste = ?'
                   ' WHERE id = ?', (beschreibung, link, anzahl, bild, preis, liste, wish_id))
    db.commit()
    return jsonify({'message': "Successfully updated id=" + str(wish_id)})


@wish.route('/sort/', methods=['POST'])
@login_required
def sort_wish():
    data = request.json

    if type(data) != list:
        return jsonify({'message': "No list provided"}), 500

    db = get_db()
    cursor = db.cursor(prepared=True)

    i = 0
    while i < len(data):
        print(str(i) + " " + data[i])
        cursor.execute('UPDATE wunschliste SET wichtigkeit = ? WHERE id = ?', (i, data[i]))
        i = i + 1

    db.commit()

    return jsonify({'message': "Successfully updated"})


@wish.route('/<int:wish_id>', methods=['DELETE'])
@login_required
def delete_wish(wish_id):
    db = get_db()
    cursor = db.cursor(prepared=True)
    cursor.execute('DELETE FROM wunschliste WHERE id = ?', (wish_id,))
    db.commit()
    return jsonify({'message': "Successfully removed id=" + str(wish_id)})
