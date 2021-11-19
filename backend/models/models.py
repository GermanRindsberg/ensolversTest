from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from werkzeug.security import generate_password_hash, check_password_hash



db = SQLAlchemy()


class User(db.Model):

    id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    name= db.Column(db.String(50))
    email= db.Column(db.String(200), unique=True)
    password= db.Column(db.String(66))
    folders= db.relationship('Folder', backref='usuario')

        
    def create_password(password):
            return generate_password_hash(password)
    def verificarPassword(self, password):
            return check_password_hash(self.password, password)
    
class Folder(db.Model):
    id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    name= db.Column(db.String(50),unique=True)
    userId=db.Column(db.Integer, db.ForeignKey('user.id'))
    tasks= db.relationship('Task', backref='carpeta')


class Task(db.Model):
    id= db.Column(db.Integer, primary_key=True, autoincrement=True)
    name= db.Column(db.String(100))
    finished = db.Column(db.Integer)
    folderId= db.Column(db.Integer, db.ForeignKey('folder.id'))
    
       
               



    