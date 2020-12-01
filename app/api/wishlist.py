import json
import os

from flask import request, jsonify, Blueprint
from app.db import get_db

from app.auth import login_required

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
    return jsonify({'status': 200, 'data': result})


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
        return jsonify({'status': 500, 'message': "Description missing"})
    if link == "":
        return jsonify({'status': 500, 'message': "Link missing"})
    if bild == "":
        return jsonify({'status': 500, 'message': "Image missing"})
    if preis == "":
        return jsonify({'status': 500, 'message': "Price missing"})
    if anzahl == "":
        return jsonify({'status': 500, 'message': "Number missing"})

    try:
        float(preis)
    except ValueError:
        return jsonify({'status': 500, 'message': "Price is no number"})

    try:
        int(anzahl)
    except ValueError:
        return jsonify({'status': 500, 'message': "Number is no integer"})

    db = get_db()
    cursor = db.cursor(prepared=True)
    cursor.execute('SELECT * FROM wunschliste WHERE link = ? AND liste = ?', (link, wish_list))
    result = cursor.fetchall()

    if len(result) == 0:
        cursor.execute()
        cursor.execute('INSERT INTO wunschliste (beschreibung, link, anzahl, bild, preis, liste) '
                       'VALUES (?, ?, ?, ?, ?, ?)', (beschreibung, link, anzahl, bild, preis, wish_list))
        wish_id = cursor.getlastrowid()
        db.commit()
        return jsonify({'status': 200, 'message': "Successfully added id=" + str(wish_id)})
    else:
        return jsonify({'status': 500, 'message': "Already in list"})


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
        return jsonify({'status': 500, 'message': "Description missing"})
    if link == "":
        return jsonify({'status': 500, 'message': "Link missing"})
    if bild == "":
        return jsonify({'status': 500, 'message': "Image missing"})
    if preis == "":
        return jsonify({'status': 500, 'message': "Price missing"})
    if anzahl == "":
        return jsonify({'status': 500, 'message': "Number missing"})
    if liste == "":
        return jsonify({'status': 500, 'message': "List missing"})

    try:
        float(preis)
    except ValueError:
        return jsonify({'status': 500, 'message': "Price is no number"})

    try:
        int(anzahl)
    except ValueError:
        return jsonify({'status': 500, 'message': "Number is no integer"})

    db = get_db()
    cursor = db.cursor(prepared=True)
    cursor.execute('UPDATE wunschliste SET beschreibung = ?, link = ?, anzahl = ?, bild = ?, preis = ?, liste = ?'
                   ' WHERE id = ?', (beschreibung, link, anzahl, bild, preis, liste, wish_id))
    db.commit()
    return jsonify({'status': 200, 'message': "Successfully updated id=" + str(wish_id)})


@wish.route('/<int:wish_id>', methods=['DELETE'])
@login_required
def delete_wish(wish_id):
    db = get_db()
    cursor = db.cursor(prepared=True)
    cursor.execute('DELETE FROM wunschliste WHERE id = ?', (wish_id,))
    db.commit()
    return jsonify({'status': 200, 'message': "Successfully removed id=" + str(wish_id)})
