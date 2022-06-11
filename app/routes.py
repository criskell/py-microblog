from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user

from app import app
from app.forms import LoginForm
from app.models import User


@app.route('/')
def index():
    user = {'username': 'criskell'}
    posts = [
        {
            'author': { 'username': 'criskell' },
            'body': 'Aprendendo Flask!'
        },
        {
            'author': { 'username': 'criskell' },
            'body': 'Preciso fazer as lições de casa!'
        }
    ]
    return render_template('index.html', title='Página inicial', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(username=form.username.data).first()

        if user is None or user.check_password(form.password.data):
            flash("O nome de usuário ou senha está inválido.")
            return redirect(url_for("login"))

        login_user(user, remember_me=form.remember_me.data)

        return redirect(url_for("index"))

    return render_template('login.html', title='Entrar', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

