from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required

from app import app
from app.forms import LoginForm
from app.models import User
from app.util import is_absolute_url


@app.route('/')
@login_required
def index():
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
    return render_template('index.html', title='Página inicial', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()

    if form.validate_on_submit():
        # Se o usuário não existir com este nome ou se a senha não
        # corresponder com o hash do usuário, redirecionamos
        # para a página de login.
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash("O nome de usuário ou senha está inválido.")
            return redirect(url_for("login"))

        # Salva o estado de login do usuário
        login_user(user, remember=form.remember_me.data)

        # Redireciona o usuário para a página anterior (ou para a página inicial)
        # a partir do argumento `next` da URL (trazido pelo decorator `login_required`).
        next_url = request.args.get('next')

        if next_url is None or is_absolute_url(next_url):
            next_url = url_for('index')

        return redirect(next_url)

    return render_template('login.html', title='Entrar', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

