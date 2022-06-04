from flask import render_template, flash, redirect, url_for

from app import app
from app.forms import LoginForm


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
    form = LoginForm()

    if form.validate_on_submit():
        flash("Os dados foram enviados com sucesso. Seu usuário é {} e sua senha é {}"
            .format(form.username.data, form.password.data))
        redirect(url_for("index"))

    return render_template('login.html', title='Entrar', form=form)