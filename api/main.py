from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from datetime import timedelta
from flask_cors import CORS
from flaskext.mysql import MySQL
from random import random

mysql = MySQL()


application = Flask(__name__)
application.debug = True
application.config['SECRET_KEY'] = 'superdupergeheimesleutel'
application.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
# MySQL configurations
application.config['MYSQL_DATABASE_USER'] = 'mym'
application.config['MYSQL_DATABASE_PASSWORD'] = 'blabladingeshoi'
application.config['MYSQL_DATABASE_DB'] = 'mym'
application.config['MYSQL_DATABASE_HOST'] = 'aitai.nl'
application.config['MYSQL_DATABASE_PORT'] = 14163
mysql.init_app(application)

class User(object):
    def __init__(self, id, email, password=0):
        self.id = id
        self.email = email
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

user_id = None

def authenticate(username, password):
    if username and password:
        conn = None
        cursor = None
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("select wachtwoord, id, email from professional where email=%s", username)
            row = cursor.fetchone()

            if check_password_hash(row[0], password):
                global user_id
                user_id = row[1]
                user = User(row[1], row[2])
                return user
            else:
                return None
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
    return None
    # bla = User(1, username, password)
    # return bla

def identity(payload):
    return user_id
    # user_id = payload['identity']
    # return userid_table.get(user_id, None)
CORS(application)

jwt = JWT(application, authenticate, identity)

@application.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity


import pymysql
# from app import app
# from db_config import mysql
from flask import jsonify
from flask import flash, request
# from werkzeug import generate_password_hash, check_password_hash
from werkzeug.security import check_password_hash, generate_password_hash

@application.route('/add', methods=['POST'])
@jwt_required()
def add_user():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        _json = request.json
        _voornaam = _json['voornaam']
        _achternaam = _json['achternaam']
        _email = _json['email']
        _wachtwoord = _json['wachtwoord']
        # validate the received values
        if _voornaam and _achternaam and _email and _wachtwoord and request.method == 'POST':
            #do not save password as a plain text
            _hashed_password = generate_password_hash(_wachtwoord)
            # save edits
            sql = "INSERT INTO professional(voornaam, achternaam, email, wachtwoord) VALUES(%s, %s, %s, %s)"
            data = (_voornaam, _achternaam, _email, _hashed_password)
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('User added successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@application.route('/users')
@jwt_required()
def users():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM professional")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@application.route('/user/<int:id>')
@jwt_required()
def user(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM professional WHERE user_id=%s", id)
        row = cursor.fetchone()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@application.route('/update', methods=['POST'])
@jwt_required()
def update_user():
    conn = None
    cursor = None
    try:
        _json = request.json
        _id = _json['id']
        _voornaam = _json['voornaam']
        _achternaam = _json['achternaam']
        _email = _json['email']
        _wachtwoord = _json['wachtwoord']
        # validate the received values
        if _voornaam and _achternaam and _email and _wachtwoord and _id and request.method == 'POST':
            #do not save password as a plain text
            _hashed_password = generate_password_hash(_wachtwoord)
            # save edits
            sql = "UPDATE professional SET voornaam=%s, achternaam=%s, email=%s, wachtwoord=%s WHERE id=%s"
            data = (_voornaam, _achternaam, _email, _hashed_password, _id)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('User updated successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@application.route('/delete/<int:id>')
@jwt_required()
def delete_user(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM professional WHERE id=%s", id)
        conn.commit()
        resp = jsonify('User deleted successfully!')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@application.route('/fake')
# @jwt_required()
def fake_data():
    data = [ round(random()*10, 1) for i in range(20) ]
    message = {
        'hoi':[
            {'name': 'Yomom',
             'data': data[:10]},
            {'name': 'Isfat',
             'data': data[10:]}
        ]
    }
    resp = jsonify(message)
    return resp

@application.route('/addpatient', methods=['POST'])
@jwt_required()
def add_patient():
    conn = None
    cursor = None
    try:
        _json = request.json
        _voornaam = _json['voornaam']
        _achternaam = _json['achternaam']
        _email = _json['email']
        _geboortedatum = _json['geboortedatum']
        _geslacht = _json['geslacht']
        _wachtwoord = _json['wachtwoord']
        if _voornaam and _achternaam and _email and _geboortedatum and _geslacht and _wachtwoord and request.method == 'POST':
            #do not save password as a plain text
            _hashed_password = generate_password_hash(_wachtwoord)
            # save edits
            sql = "INSERT INTO patient(voornaam, achternaam, email, geboortedatum, wachtwoord, geslacht) VALUES(%s, %s, %s, %s, %s, %s)"
            data = (_voornaam, _achternaam, _email, _geboortedatum, _hashed_password)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('User updated successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@application.route('/test', methods=['GET'])
@jwt_required()
def test():
    id = request.args.get('id')
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM professional where id=%s", id)
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@application.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp

if __name__ == "__main__":
    application.run()
