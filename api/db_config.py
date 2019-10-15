from main import app
from flaskext.mysql import MySQL

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'mym'
app.config['MYSQL_DATABASE_PASSWORD'] = 'blabladingeshoi'
app.config['MYSQL_DATABASE_DB'] = 'mym'
app.config['MYSQL_DATABASE_HOST'] = 'aitai.nl'
app.config['MYSQL_DATABASE_PORT'] = 14163
mysql.init_app(app)
