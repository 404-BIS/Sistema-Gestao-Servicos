from flask import Flask, redirect, url_for,session
from flask_login import LoginManager, logout_user
from bd.db import mysql

from pasta_user.user import user_blueprint
from pasta_executor.executor import executor_blueprint
from pasta_login.login import main
from pasta_cadastro.cadastro import auth
from pasta_adm.adm import admin

import secrets

app = Flask(__name__)

secret = secrets.token_urlsafe(32)
app.secret_key = secret

# UPLOAD_FOLDER = 'static/uploads/'
 
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024

# ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



app.register_blueprint(user_blueprint)
app.register_blueprint(executor_blueprint)
app.register_blueprint(main)
app.register_blueprint(auth)
app.register_blueprint(admin)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)



@login_manager.user_loader
def load_user(id_user):
    return mysql.get(id_user)


@app.route("/logout")
def logout():
    session['loggedin'] = False
    logout_user()
    return redirect(url_for('auth.login'))

if __name__ == "__main__":
    app.run(debug=True)