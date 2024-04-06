#Importando librerias necesarias para el proyecto
from flask import Flask,render_template,redirect,url_for,request,flash
from config import ObjectConfig
from flask_login import LoginManager,logout_user,login_required,login_user
from flask_mysqldb import MySQL

#Models
from models.ModelUser import ModelUser
from models.DataGraphs import DataGraphs

#Entities
from models.entities.User import User

app=Flask(__name__)
db=MySQL(app)
managgerloggin=LoginManager(app)

@managgerloggin.user_loader
def user_loader(id):
    return ModelUser.get_by_id(db,id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        user=User(None,request.form['Username'],request.form['Password'])
        userlogged=ModelUser.LoggedUser(db,user)
        if userlogged !=None:
            if userlogged.password:
                login_user(userlogged)
                return redirect(url_for('home'))
            
            else:
                flash('Incorrect password')
                return render_template('Auth/login.html')
            
        else:
            flash('User not found')
            return render_template('Auth/login.html')
    
    else:
        return render_template('Auth/login.html')
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    return render_template('HomeMain.html')



@app.route('/plot')
@login_required
def plot():
    data=DataGraphs.HistogramJson(db)

    return render_template('AnimalsHered.html',data=data)


if __name__=='__main__':
    app.config.from_object(ObjectConfig)
    app.run()