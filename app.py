from flask import Flask, render_template, redirect, request, Response, session
from flask_mysqldb import MySQL, MySQLdb
from sqlalchemy import text, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from signos import Base, usuario

engine = create_engine("postgresql://SurData_admin:SignosMaga2808@signos-db.ctqemoeacw1f.eu-north-1.rds.amazonaws.com:5432/postgres")
Session = sessionmaker(bind=engine)
db_session = Session()
Base = declarative_base()

app = Flask(__name__)

app.secret_key = "super_secreto"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    # Buscamos el usuario en la tabla
    user = db_session.query(usuario).filter_by(nombre=username, contrasena=password).first()

    if user:
        session['username'] = user.nombre
        session['rol'] = user.rol
         
         # Redirigimos según el rol
        if user.rol == 'duena':
            return redirect('/home_duena')
        elif user.rol == 'secretaria':
            return redirect('/home_secretaria')
        elif user.rol == 'HC':
            return redirect('/home_hc')
        elif user.rol == 'electrocardiograma':
            return redirect('/home_electrocardiograma')
        elif user.rol == 'fonoaudiologia':
            return redirect('/home_fonoaudiologia')
        elif user.rol == 'psicologia':
            return redirect('/home_psicologia')
        elif user.rol == 'medico':
            return redirect('/home_medico')
        else:
            return "No hay pagina para tu rol comunicate con la tecnica en Data Science"
    else:
        return "Usuario o contraseña incorrectos"

@app.route('/home')
def home():
    if 'username' in session:
        return f"Bienvenido {session['username']}! Tu rol es: {session['rol']}"
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.secret_key= "gabriel_hds"
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)

