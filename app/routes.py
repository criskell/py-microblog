# parei no capitulo 2

from flask import render_template
from app import app

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