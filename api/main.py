from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from datetime import timedelta
from flask_cors import CORS
from flaskext.mysql import MySQL
import random
import datetime
import pymysql
from flask import jsonify
from flask import flash, request
from werkzeug.security import check_password_hash, generate_password_hash

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
CORS(application)

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

def identity(payload):
    return user_id

jwt = JWT(application, authenticate, identity)

@application.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity


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
            # do not save password as a plain text
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
            # do not save password as a plain text
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
@jwt_required()
def fake_data():
    data = [ round(random.normalvariate(8, .1), 1) for i in range(14) ]
    message = {
        'hoi':[
            {'name': 'Yomom',
             'data': data[:7]},
            {'name': 'Isfat',
             'data': data[7:]}
        ]
    }
    resp = jsonify(message)
    return resp

@application.route('/bla')
def bla():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select id from professional where id=1")
    row = cursor.fetchone()
    print(row[0])
    return "<H1>Bla</H1>"

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
        _bsn = _json['bsn']
        if _voornaam and _achternaam and _email and _geboortedatum and _geslacht and _wachtwoord and _bsn and request.method == 'POST':
            print("post enzo")
            # do not save password as a plain text
            _hashed_password = generate_password_hash(_wachtwoord)
            # insert patient info into db
            sql = "INSERT INTO patient(voornaam, achternaam, email, geboortedatum, wachtwoord, geslacht, bsn) VALUES(%s, %s, %s, %s, %s, %s, %s)"
            data = (_voornaam, _achternaam, _email, _geboortedatum, _hashed_password, _geslacht, _bsn)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)

            # get the generated id for the patient
            cursor.execute("select id from patient where email=%s", _email)
            row = cursor.fetchone()

            # connect the currently logged in professional to the just added patient
            data = (row[0], str(current_identity))
            cursor.execute("insert into patient_professional(patient_id, professional_id) values(%s, %s)", data)
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

@application.route('/disablepatient', methods=['POST'])
@jwt_required()
def disablepatient():
    conn = None
    cursor = None
    _json = request.json
    _id = _json['id']
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        # check if patient exists and belongs to currently logged in professional
        data = (_id, current_identity)
        cursor.execute("select p.id from patient p join patient_professional pa on pa.patient_id = p.id join professional pr on pr.id = pa.professional_id where p.id=%s and pr.id=%s", data)
        row = cursor.fetchone()

        # if above is true:
        if row:
            sql  ="update patient set uitgeschakeld=%s where id=%s"
            data = (datetime.datetime.now(), _id)
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('User disabled successfully!')
            resp.status_code = 200
            return resp

        resp = jsonify('Patient does not belong to currently logged in professional')
        resp.status_code = 500
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@application.route('/patients', methods=['GET'])
@jwt_required()
def patients():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute("select * from patient p join patient_professional pa on pa.patient_id = p.id join professional pr on pr.id = pa.professional_id where pr.id=%s", current_identity)
        rows = cursor.fetchall()
        print(rows)
        resp = jsonify(rows)
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@application.route('/test', methods=['GET', 'POST'])
@jwt_required()
def test():
    id = request.args.get('id')
    conn = None
    cursor = None
    if request.method=='GET':
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
