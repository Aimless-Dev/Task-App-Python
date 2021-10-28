from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '220030070'
app.config['MYSQL_DB'] = 'flaskapp'
mysql = MySQL(app)

app.secret_key = "mysecretkey"

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tarea')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', data = data)

@app.route('/add', methods=['POST'])
def add_task():
    if request.method == 'POST':
        task = request.form['task']
        des = request.form['des']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO tarea (nombre, descripcion) VALUES (%s, %s)', (task, des))
        mysql.connection.commit()
        flash('Tarea agregada')
        return redirect(url_for('index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_task(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM tarea WHERE id = {0}'.format(id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-task.html', data = data[0])


@app.route('/update/<id>', methods = ['POST'])
def update_task(id):
    if request.method == 'POST':
        task = request.form['task']
        des = request.form['des']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE tarea SET nombre = %s, descripcion = %s WHERE id = %s', (task, des, id))
        flash('Tarea actualizada')
        mysql.connection.commit()
        return redirect(url_for('index'))


@app.route('/delete/<string:id>', methods = ['POST', 'GET'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM tarea WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Tarea eliminada')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(port=8080, debug=True)