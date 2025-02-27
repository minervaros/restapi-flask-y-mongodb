from flask import Flask, jsonify, redirect
from flask_pymongo import PyMongo
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuración de MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/testdb"
mongo = PyMongo(app)

# Configuración de MySQL
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "patata"
app.config["MYSQL_DB"] = "testdb"
mysql = MySQL(app)

@app.route("/")
def home():
    return redirect("/mongo_objects")

# Obtener 4 objetos de MongoDB
@app.route("/mongo_objects", methods=["GET"])
def get_mongo_objects():
    objects = list(mongo.db.objects.find({}, {"_id": 0}))[:4]
    return jsonify(objects)

# Obtener 4 objetos de MySQL
@app.route("/mysql_objects", methods=["GET"])
def get_mysql_objects():
    cur = mysql.connection.cursor()
    cur.execute("SELECT name FROM objects LIMIT 4")
    objects = [row[0] for row in cur.fetchall()]
    cur.close()
    return jsonify(objects)

if __name__ == "__main__":
    app.run(debug=True)
