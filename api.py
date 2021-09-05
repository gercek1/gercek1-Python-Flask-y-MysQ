from flask import Flask,render_template,url_for, redirect,flash
from flask.globals import request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '320732'
app.config['MYSQL_DB'] = 'flaskcontact'
mysql = MySQL(app)

app.secret_key = 'secretkey'


@app.route('/')
def index():
    go = mysql.connection.cursor()
    go.execute('SELECT * FROM contactos')
    data = go.fetchall()
    return render_template("portada.html", contactos = data)

@app.route("/contactos", methods=['POST'])
def addContactos():
    if request.method == 'POST':
        name = request.form['name']
        apellido = request.form['ape']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contactos(nombre,apellido,telefono,correo) VALUES (%s, %s, %s,%s)",
        (name,apellido,phone,email))
        mysql.connection.commit()
        flash('Contacto agregado')
        return redirect(url_for('index'))

@app.route("/delete/<string:id>")
def deleteConta(id):
   cur = mysql.connection.cursor()
   cur.execute("DELETE FROM contactos WHERE id = {0}".format(id))
   mysql.connection.commit()
   flash('contacto eliminado')
   return redirect(url_for('index'))

@app.route("/edit/<id>")
def getDato(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactos WHERE id = %s', (id))
    data = cur.fetchall()
    return render_template('editar.html', contactos = data[0])

@app.route("/actualizar/<id>", methods=['POST'])
def actualizar(id):
    if request.method == 'POST':
        fullname = request.form['name']
        apellido = request.form['ape']
        telefono = request.form['phone']
        correo = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
          UPDATE contactos
          SET nombre = %s,
            apellido = %s,
            telefono = %s,
            correo = %s
          WHERE id = %s
        """,(fullname,apellido,telefono,correo,id))
        mysql.connection.commit()   
        flash('contacto actualizado') 
        return redirect(url_for('index'))





if __name__ == '__main__':
    app.run(port = 3000, debug=True)

