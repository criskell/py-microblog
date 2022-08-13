from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from datetime import datetime

from app import app, db
from app.forms import EditProfileForm, LoginForm, RegistrationForm, EmptyForm
from app.models import User
from app.util import is_absolute_url

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForm()
    
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)

        user.set_password(form.password.data)

        db.session.add(user)
        db.session.commit()

        flash('Parabéns. Você criou uma conta')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Registrar-se', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()

    posts = [
        {
            'author': user,
            'body': 'Aprendendo Flask!'
        },
        {
            'author': user,
            'body': 'Preciso fazer as lições de casa!'
        }
    ]

    form = EmptyForm()

    return render_template('user.html', title='Perfil', user=user, posts=posts, form=form)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('As alterações foram salvas com sucesso.')
        return redirect(url_for('edit_profile'))

    if request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    
    return render_template('edit_profile.html', title='Editar perfil', form=form)

@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('Usuário {} não encontrado.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('Não é possível seguir a si mesmo.')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('Você está seguindo {}!'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))

@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('Usuário {} não encontrado.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('Você não pode dar unfollow em si próprio!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('Você não está mais seguindo {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))