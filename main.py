import flask
import MySQLdb.cursors
from flask import url_for
from flask_mysqldb import MySQL
import re

app = flask.Flask(__name__)
app.secret_key = "XXXXXXXX"
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = ""
app.config['MYSQL_DB'] = "flask"
mysql = MySQL(app)

@app.route('/login', methods=['GET', 'POST'])
def login():
	msg_error = ""
	if flask.request.method == "POST" and "username" in flask.request.form and "password" in flask.request.form:
		username = flask.request.form["username"]
		password = flask.request.form["password"]
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password,))
		user = cursor.fetchone()
		if user:
			flask.session["log"] = True
			flask.session["id"] = user["id"]
			flask.session["username"] = user["username"]
			return flask.redirect("/home")
		else:
			msg_error = "Il y a eu une erreur, veuillez réessayer!"
	return flask.render_template("login.html", msg=msg_error)

@app.route('/logout')
def logout():
	flask.session.pop("log", None)
	flask.session.pop("id", None)
	flask.session.pop("username", None)
	return flask.redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
	msg_error = ""
	if flask.request.method == "POST" and "username" in flask.request.form and "password" in flask.request.form:
		username = flask.request.form["username"]
		password = flask.request.form["password"]
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
		user = cursor.fetchone()
		if user:
			msg_error = "Nom d'utilisateur déjà pris!"
		elif not re.match(r"[a-zA-Z0-9]", username):
			msg_error = "Votre pseudo n'a pas les bons caractères!"
		elif not re.match(r"[a-zA-Z0-9]", password):
			msg_error = "Vote mot de passe n'a pas les bons caractères!"
		else:
			cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
			cursor.execute("INSERT INTO users VALUES(NULL, %s, %s)", (username, password,))
			mysql.connection.commit()
			return flask.redirect(url_for('login'))
	return flask.render_template("register.html", msg=msg_error)

@app.route('/home')
def home():
	if "log" in flask.session:
		username = flask.session["username"]
		return flask.render_template('home.html', username=username)
	else:
		return flask.redirect(url_for('login'))
if __name__ == "__main__":
	app.run(host="127.0.0.1", port=1337, debug=True)
