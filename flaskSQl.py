from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy as sqal
app = Flask(__name__)

#MYSQL Configurations hosted on freesqlhosting
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://sql12395470:zizg45JrB2@sql12.freemysqlhosting.net/sql12395470'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#MYSQL Config End

#POSTGRESQL Configurations hosted on ElephantSQL
app.config['SQLALCHEMY_BINDS'] = {'postgresql': 'postgres://zzhztkzc:ZIX_KpogxSOQhxKKtMXCxvp3AqURAQG0@rogue.db.elephantsql.com:5432/zzhztkzc'}
#POSTGRESQL config End

app.config['SECRET_KEY'] = 'asdfghjkl'

mysql = sqal(app)

#MYSQL Class/Model
class UserInfo(mysql.Model):
    id = mysql.Column(mysql.Integer, primary_key=True)
    name = mysql.Column(mysql.String(100))
    age = mysql.Column(mysql.String(100))

    def __init__(self, name, age):
        self.name = name
        self.age = age
#MYSQL Class/Model End

#POSTGRESQL Class/Model
class UserDetail(mysql.Model):
    __bind_key__='postgresql'
    id = mysql.Column(mysql.Integer, primary_key=True)
    name = mysql.Column(mysql.String(100))
    email = mysql.Column(mysql.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email
#POSTGRESQL Class/Model End



@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/MySQL', methods=['GET', 'POST'])
def mysqlrt():
    if request.method == "POST":
        userI = UserInfo(request.form['name'], request.form['age'])
        try:
            mysql.session.add(userI)
            mysql.session.commit()
        except:
            flash("Name already in Database")
    try:
        if request.method == "GET":
            return render_template('MySQL.html', users=UserInfo.query.all())
    except:
        return "Error in town"
    return render_template('MySql.html', users=UserInfo.query.all())


@app.route('/PostgreSQL', methods=['POST', 'GET'])
def postgre():
    if request.method == "POST":
        userI = UserDetail(request.form['name'], request.form['email'])
        try:
            mysql.session.add(userI)
            mysql.session.commit()
        except:
            flash("Name already in Database")
    try:
        if request.method == "GET":
            return render_template('postgresql.html', users=UserDetail.query.all())
    except:
        return "Error in town"
    return render_template('postgresql.html', users=UserDetail.query.all())


if __name__ == '__main__':
    mysql.create_all()
    app.run()
