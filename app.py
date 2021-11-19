from flask import Flask, render_template, request, redirect, flash, url_for, session
from backend.models.models import db, User, Task, Folder

app = Flask(__name__, template_folder="frontend/templates")


app.config.from_object("backend.config.DevelepmentConfig")

app.static_url_path=app.config.get('STATIC_FOLDER')
db.init_app(app)

with app.app_context():
        db.create_all()


@app.route("/")
def index():
    if 'name' in session:
        show='hide'
        folderName=''
        uid= str( session['userId'])
        folders=Folder.query.filter(Folder.userId == uid).all()
        return render_template('principal.html', show=show, folders=folders,folderName=folderName)
    else:
        show='show'
        folderName=''
        return render_template('principal.html', show=show, folderName=folderName)

@app.route("/submit", methods=['POST'])
def login():
   
    email=request.form['inputEmail']
    password= request.form['inputPassword']

    user = User.query.filter_by(email=email).first()
    if user is not None and User.verificarPassword(user,password):
        session['name'] = user.name
        session['userId'] = user.id
        return redirect('/')
    else:
        return redirect('/')

@app.route("/register")
def register():
    return render_template('/register.html')
    
@app.route("/reg" ,methods=['POST'])
def reg():
    name=request.form['txtName']
    mail=request.form['txtEmail']
    pw=request.form['txtPass']
    user= User(name=name, email=mail, password= User.create_password(pw))
    db.session.add(user)
    db.session.commit()
    user = User.query.filter_by(email=mail).first()
    session['name']= request.form['txtName']
    session['userId'] = user.id
    
    return redirect ('/')
    
@app.route("/logout")
def logout():
    if session['name']:
        session.clear()
        return redirect('/')
    else:    
        return redirect('/')

@app.route("/newFolder",methods=['POST'])
def newFolder():
    if request.form['folderName']!='':
        id= str(session['userId'])
        user = User.query.filter(User.id == id).first()
        
        folderName=request.form['folderName']
        folder= Folder(name=folderName, usuario=user )
        db.session.add(folder)
        db.session.commit()
        return redirect('/')
    else:
        return redirect ('/')

@app.route("/newTask/<int:id>" , methods=['POST'])
def newTask(id):
    if request.form['taskName']!='':
        folderName=Folder.query.filter(Folder.id == id).first()
        taskName=request.form['taskName']
        task= Task(name=taskName, carpeta=folderName )
        db.session.add(task)
        db.session.commit()
        direccion=str('/items/'+str(id))
        return redirect(direccion)
    else:
        return redirect ('/')

@app.route('/items/<int:id>')
def verItems(id):

    items=Task.query.filter(Task.folderId == id ).all()
    show='hide'
    folderName=Folder.query.filter(Folder.id == id).first()

    if db.session.query(Folder).all():
        folders = Folder.query.filter(Folder.userId == session['userId'] ).all()
        items= Task.query.filter(Task.folderId == id).all()
        
        session['carpetaId']=id
        return render_template('principal.html', show=show, folders=folders, items=items, folderName=folderName)
    else:
        return render_template('principal.html', show=show)

@app.route("/editTask", methods=['POST'])
def editTask():
        taskName=request.form['txtTask']
        taskId=request.form['txtId']
        task = Task.query.filter_by(id=taskId).first()
        task.name=taskName
        db.session.commit() 

        direccion=str('/items/'+str(task.folderId))
        return redirect(direccion)

@app.route("/finished/<int:id>", methods=['POST'])
def finished(id):
    task = db.session.query(Task).filter(Task.id == id).first()
    if task.finished==1:
        task.finished=0    
    else:    
        task.finished=1
    
    db.session.commit()
    direccion=str('/items/'+str(task.folderId))
    return redirect(direccion)
    
@app.route('/destroyFolder/<int:id>')
def destroy(id):
    Folder.query.filter(Folder.id == id).delete()
    Task.query.filter(Task.folderId == id).delete()
    db.session.commit()
    return redirect('/')
    
@app.route('/destroyTask/<int:id>')
def destroyTask(id):
    task = Task.query.filter_by(id=id).first()
    direccion=str('/items/'+str(task.folderId))
  
    Task.query.filter(Task.id == id).delete()
    db.session.commit()
   
    return redirect(direccion)

if __name__ == '__main__':    app.run()

