from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from datetime import timedelta
from flask_cors import CORS
from flaskext.mysql import MySQL
import random
from datetime import datetime
import base64
import pymysql
import requests, sched, time, threading
from flask import jsonify
from flask import flash, request
from werkzeug.security import check_password_hash, generate_password_hash
import json

mysql = MySQL()
s = sched.scheduler(time.time, time.sleep)

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

@application.route('/refresh_fitbit_token', methods=['POST'])
@jwt_required()
def refresh_fitbit_token():
    _json = request.json
    _id = _json['id']
    if _id and request.method == 'POST':
        return refresh_fitbit_token_local(_id)
    else:
        return not_found()

def refresh_fitbit_token_local(id):
    conn = None
    cursor = None
    url = 'https://api.fitbit.com/oauth2/token'
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": "Basic MjJCNVhYOmVjYzdiOWNmODk0ZjJhOTZiYzg4OWJkZjQxOTQwYTQ4"}
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT refresh_token FROM fitbit_auth WHERE patient_id=%s", id)
        refresh_token = cursor.fetchone()["refresh_token"]
        data = {'grant_type': 'refresh_token', 'refresh_token': refresh_token}
        req = requests.post(url, data=data, headers=headers)
        out=json.loads(req.text)
        # print(out)
        if "access_token" in out.keys():
            print(2)
            sql = "UPDATE fitbit_auth SET access_token=%s, refresh_token=%s WHERE patient_id=%s"
            resp = (out["access_token"], out["refresh_token"], id)
            cursor.execute(sql, resp)
            conn.commit()
            return out["access_token"]
        else:
            return ({"error","An error occurred while refreshing FitBit access token."})
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@application.route('/loginPatient', methods=['POST'])
def login():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        _json = request.json
        _username = _json['email']
        _password = _json['wachtwoord']
        if _username and _password:
            cursor.execute("select wachtwoord, id, email from patient where email=%s", _username)
            row = cursor.fetchone()
            if check_password_hash(row[0], _password):
                resp = jsonify({"id": row[1]})
                resp.status_code = 200
                return resp
            else:
                resp = jsonify("Login failed!")
                resp.status_code = 401
                return resp
        else:
            resp = jsonify('Username or password is missing')
            return resp
    except Exception as e:
        resp = jsonify('error')
        return resp
    finally:
        cursor.close()

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

@application.route('/isAdmin')
@jwt_required()
def isAdmin():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT admin_id FROM professional where id=%s", str(current_identity))
        rows = cursor.fetchone()
        if rows[0]:
            resp = "True"
            jsonify(resp)
            return jsonify(resp)
        else:
            resp = "False"
            jsonify(resp)
            return jsonify(resp)
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

        cursor.execute("select * from patient p join patient_professional pa on pa.patient_id = p.id join professional pr on pr.id = pa.professional_id where pr.id=%s", str(current_identity))
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

@application.route('/saveEmotionReport', methods=['POST'])
def saveEmotionReport():
    conn = None
    cursor = None
    try:
        _patient_id = request.json['PatientId']
        _date = request.json['Date']
        _partofday = request.json['PartOfDay']
        _painlevel = request.json['PainLevel']
        _happy = request.json['Happy']
        _angry = request.json['Angry']
        _scared = request.json['Scared']
        _energetic = request.json['Energetic']
        _tired = request.json['Tired']
        _feeling = request.json['EmoticonType']
        _notes = request.json['Notes']
        if _patient_id and _date and _partofday and _painlevel and _angry and _happy and _energetic and _tired and _scared and _feeling and request.method == "POST":
            sql = "INSERT INTO emotierapport(patient_id, date, dagdeel, pijnniveau, boos, blij, energiek, moe, bang, gevoel) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            data = (_patient_id, _date, _partofday, _painlevel, _angry, _happy, _energetic, _tired, _scared, _feeling)
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute(sql, data)
            conn.commit()
            emotionID = cursor.lastrowid
            for note in _notes:
                sql = "INSERT INTO emotierapport_note(emotierapport_id, note_id) VALUES(%s, (SELECT id FROM note WHERE text=%s))"
                data = (emotionID, note)
                cursor.execute(sql, data)
                conn.commit()
            rows = cursor.fetchall()
            resp = jsonify("Emotionreport saved.")
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        resp = jsonify("Emotionreport could not be saved.")
        resp.status_code = 401
    finally:
        cursor.close()
        conn.close()


@application.route('/emotionReport/<int:patient_id>/date/<string:date>')
def getEmotionReport(patient_id, date):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        data = (patient_id, date)
        cursor.execute("SELECT id, patient_id AS PatientId, date AS Date, dagdeel AS PartOfDay, pijnniveau AS PainLevel, boos AS Angry, blij AS Happy, energiek AS Energetic, moe AS Tired, bang AS Scared, gevoel AS EmoticonType FROM emotierapport WHERE patient_id=%s AND date=%s", data)
        row = cursor.fetchall()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        resp = jsonify(e)
        resp.status_code = 402
    finally:
        cursor.close()
        conn.close()

@application.route('/emotionReportNotes/<int:emotionReport_id>')
def getEmotionReportNotes(emotionReport_id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT text FROM note INNER JOIN emotierapport_note ON id = note_id WHERE emotierapport_id = %s", emotionReport_id)
        row = cursor.fetchall()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        resp = jsonify(e)
        resp.status_code = 402
    finally:
        cursor.close()
        conn.close()

@application.route('/getEmotionReportPeriod')
def getEmotionReportPeriod():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        _patient_id = request.json['patient_id']
        _start_date = request.json['start_date']
        _end_date = request.json['end_date']
        data = (_patient_id, _start_date, _end_date)
        cursor.execute("SELECT * FROM emotierapport WHERE patient_id=%s AND date BETWEEN %s AND %s", data)
        row = cursor.fetchall()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@application.route('/emotionReportExists')
def getEmotionReportExists():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        _patient_id = request.json['patient_id']
        _date = request.json['date']
        _partofday = request.json['partofday']
        data = (_patient_id, _date, _partofday)
        cursor.execute("SELECT * FROM emotierapport WHERE patient_id=%s AND date=%s AND dagdeel=%s", data)
        row = cursor.fetchone()
        if row:
            resp = jsonify("true")
        else:
            resp = jsonify("false")
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@application.route('/saveNewNote', methods=['POST'])
def saveNewNote():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        print(request.json)
        _json = request.json
        _note = _json['note']
        _patient_id = _json['patient_id']

        if _note and _patient_id and request.method == "POST":
            sql = "INSERT INTO note(text) VALUES(%s)"
            data = (_note)
            cursor.execute(sql, data)

            sql = "SELECT id from note WHERE text=%s"
            cursor.execute(sql, data)

            row = cursor.fetchone()
            sql = "INSERT INTO patient_note(patient_id, note_id) VALUES(%s, %s)"
            data = (_patient_id, row[0])

            cursor.execute(sql, data)
            conn.commit()

            resp = jsonify('Note added')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@application.route('/getNotes/<int:id>', methods=['GET'])
def getNotes(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if id and request.method == "GET":
            sql = "SELECT patient_note.note_id, note.text FROM patient_note, note WHERE patient_id=%s AND note.id = patient_note.note_id"
            data = (id)
            cursor.execute(sql, data)
            row = cursor.fetchall()
            resp = jsonify(row)
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@application.route('/user/<int:user_id>/note/<string:note_text>', methods=['DELETE'])
def deleteNote(user_id, note_text):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        print(note_text)
        print(user_id)
        if user_id and note_text and request.method == "DELETE":
            sql = "DELETE FROM patient_note WHERE note_id=(SELECT id FROM note WHERE text=%s) AND patient_id=%s"
            data = (note_text, user_id)
            cursor.execute(sql, data)

            conn.commit()
            resp = jsonify('Note deleted!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@application.route('/saveAccessToken', methods=['POST'])
def saveAccessToken():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        _json = request.json
        _patient_id = _json['patient_id']
        _access_token = _json['access_token']
        _refresh_token = _json['refresh_token']
        _token_type = _json['token_type']

        if _patient_id and _access_token and _refresh_token and _token_type and request.method == "POST":
            sql = "SELECT patient_id from fitbit_auth WHERE patient_id=%s"
            cursor.execute(sql, _patient_id)
            row = cursor.fetchone()
            # Check if patient id already exists, if so overwrite accesstoken and refreshtoken, else create new entry.
            if(row):
                sql = "UPDATE fitbit_auth SET access_token = %s, refresh_token = %s WHERE patient_id = %s"
                data = (_access_token, _refresh_token, _patient_id)
            else:
                sql = "INSERT INTO fitbit_auth(patient_id, access_token, refresh_token, token_type) VALUES(%s, %s, %s, %s)"
                data = (_patient_id, _access_token, _refresh_token, _token_type)   
            cursor.execute(sql, data)

            conn.commit()

            resp = jsonify('Access token saved')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@application.route('/getFitbitToken/<int:user_id>', methods=['GET'])
def getFitbitToken(user_id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        if user_id and request.method == "GET":
            sql = "SELECT access_token FROM fitbit_auth WHERE patient_id=%s"
            data = (user_id)
            cursor.execute(sql, data)
            row = cursor.fetchone()
            access_token = checkTokenValidity(row["access_token"], user_id)            
            #only send Access code.
            resp = jsonify(access_token)
            if access_token == "":
                resp.status_code = 400 
            else:
                resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
        resp = jsonify("Api threw exception")
        resp.status_code = 400
    finally:
        cursor.close()
        conn.close
def getValidFitbitToken(access_token, id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        # Decode access token to get expire date.
        decode = base64.urlsafe_b64decode(access_token+"==")
        decodedStr = str(decode, "latin-1")
        TokenExpire = int(decodedStr.split(',')[5].split(':')[1])
        date = datetime.utcfromtimestamp(TokenExpire)
        testDate = datetime.utcfromtimestamp(TokenExpire +10)
        # if access_token is expired, refresh
        if date < testDate:
            access_token = refresh_fitbit_token_local(id)
        return(access_token)
    except Exception as e:
        print(e)
        return("")
    finally:
        cursor.close()
        conn.close



@application.route('/sendNotifications', methods=['GET'])
def startThread():
    #if we have multiple services in the queue something is wrong, clear the queue and start a new thread.
    if len(s.queue) > 0:
        stopNotifications()
    
    x = threading.Thread(target=sendNotifications, args=())
    x.start()
    return ""
        
@application.route('/stopNotifications', methods=['GET'])
def stopNotifications():
    #Remove all items from the queue
    while len(s.queue) > 0:
        s.cancel(s.queue[0])
    return ""

@application.route('/notificationServiceIsRunning', methods=['GET'])
def isRunning():
    return str(not s.empty())
    
def sendNotifications():
    now = datetime.datetime.now()
    #Only send the notifications 3 times a day.
    if now.hour == 10 or now.hour == 16 or now.hour == 22:
        try:
            headers = {'accept': 'application/json','X-API-Token': '43c80985e6f73b4a082459f78ca7b1f2b911ac6a','Content-Type': 'application/json',}
            data = '{ "notification_content": { "name": "EmotionReport", "title": "Emotierapport", "body": "Vergeet u niet uw emotierapport in te vullen?" }}'
            #Send notification to iOS devices
            responseiOS = requests.post('https://api.appcenter.ms/v0.1/apps/moveyourmind/MoveYourMind-iOS/push/notifications', headers=headers, data=data)
            #Send notification to Android devices
            responseAndroid = requests.post('https://api.appcenter.ms/v0.1/apps/moveyourmind/MoveYourMind-Android/push/notifications', headers=headers, data=data)
        except Exception as e:
            print(e)
    
    #if we have multiple services in the queue something is wrong, clear the queue before continuing
    if len(s.queue) > 0:
        stopNotifications()
        
    #Check time again in 1 hour
    s.enter(3600, 1, sendNotifications, ())
    s.run()
    
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
    # refresh_fitbit_token_local(1)
    application.run()
