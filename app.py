from nntplib import GroupInfo
from tokenize import group
from services.pbiembedservice import PbiEmbedService
from utils import Utils
from flask import Flask, render_template, send_from_directory, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json
import os

##################################################################################################################################
app = Flask(__name__)

app.config.from_object('config.BaseConfig')
app.config['SECRET_KEY'] = 'jX7Crsk9Hynevn5yXO8f3AXGFK7Pywfq!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:Citrix.54@localhost:3310/dbpbi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

class User(UserMixin, db.Model):
    id              = db.Column(db.Integer, primary_key=True)
    username        = db.Column(db.String(200), unique=True)
    name_surname    = db.Column(db.String(200))
    email           = db.Column(db.String(200), unique=True)
    password        = db.Column(db.String(200))
    group           = db.Column(db.String(200))
    is_admin        = db.Column(db.Boolean, default=False) 

    def __repr__(self):
        return self.name_surname

class LoginForm(FlaskForm):
    username = StringField('Usuário', validators=[InputRequired(), Length(min=4, max=16)])
    password = PasswordField('Senha', validators=[InputRequired(), Length(min=8, max=32)])

class RegisterForm(FlaskForm):
    GRUPOS = ['Nenhum', 'Maquinas', 'Peças', 'Controladoria']

    email           = StringField('E-mail', validators=[InputRequired(), Email(message='E-mail inválido'), Length(max=64)])
    name_surname    = StringField('Nome Completo', validators=[InputRequired(), Length(min=4, max=64)])
    username        = StringField('Usuário', validators=[InputRequired(), Length(min=4, max=16)])
    password        = PasswordField('Senha', validators=[InputRequired(), Length(min=8, max=32)])
    group           = SelectField('Grupo', validators=[InputRequired()], choices=GRUPOS)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                return '<h1>Senha incorreta</h1>'
        else:
            return '<h1>Usuário não encontrado</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data, email=form.email.data).first()
        if user:
            return '<h1>Usuário já foi criado anteriormente!</h1>'

        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user        = User(username=form.username.data, email=form.email.data, group=form.group.data, name_surname=form.name_surname.data, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

##################################################################################################################################

@app.route('/dashboard', methods=['GET'])
@login_required
def index():
    user = current_user

    return render_template('dashboard.html', user=user)

@app.route('/getembedinfo', methods=['GET'])
@login_required
def get_embed_info():
    config_result = Utils.check_config(app)

    if config_result is not None:
        return json.dumps({'errorMsg': config_result}), 500

    try:
        embed_info = PbiEmbedService().get_embed_params_for_single_report(app.config['WORKSPACE_ID'], app.config['REPORT_ID'])
        return embed_info
    except Exception as ex:
        return json.dumps({'errorMsg': str(ex)}), 500

# @app.route('/favicon.ico', methods=['GET'])
# def getfavicon():
#     return send_from_directory(os.path.join(app.root_path, 'static'), 'img/favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == '__main__':
    app.run()