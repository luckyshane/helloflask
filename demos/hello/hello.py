import click
import os
from flask import json, jsonify, session
from flask import Flask, request, redirect, url_for, abort, make_response
from jinja2.utils import generate_lorem_ipsum
from markupsafe import escape

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "secret key default")


# the minimal Flask application
@app.route('/')
def index():
    return '<h1>Hello, World!</h1>'


@app.route("/login")
def login():
    session['logged_in'] = True  # 写入session
    return redirect(url_for('say_hello'))


@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('say_hello'))


# bind multiple URL for one view function
@app.route('/hi')
@app.route('/hello')
def say_hello():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', "human")
    resp = '<h1>Hello, {}!</h1>'.format(escape(name))
    if 'logged_in' in session:
        resp += '[Authenticated]'
    else:
        resp += '[Not Authenticated]'
    return resp


@app.route('/refer')
def refer():
    return '', 302, {'Location': 'http://www.baidu.com'}


@app.route('/shake')
def shake():
    # return redirect(url_for('refer'))
    return redirect('http://www.baidu.com')


@app.route('/status')
def get_status():
    name = request.args.get('name', 'Shane')
    data = {
        'code': 0,
        'message': '{} is ok'.format(name)
    }
    resp = jsonify(data)
    return resp


@app.route("/set/<name>")
def set_cookie(name):
    resp = make_response(redirect(url_for("say_hello")))
    resp.set_cookie('name', name)
    resp.set_cookie('gender', 'male', httponly=True)
    return resp


@app.route('/404')
def not_found():
    abort(500)
    return "yeah baby!"


@app.route("/love/<any(Lily, Lucy, XiaoMing):name>")
def love(name):
    return "<p>My lover is {}</p>".format(name)


# dynamic route, URL variable default
@app.route('/greet', defaults={'name': 'Programmer'})
@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello, %s!</h1>' % name


@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(n=2)
    return '''
<h1>A very long post</h1>
<div class="body">%s</div>
<button id="load">Load More</button>
<script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
<script type="text/javascript">
$(function() {
    $('#load').click(function() {
        $.ajax({
            url: '/more',
            type: 'get',
            success: function(data){
                $('.body').append(data);
            }
        })
    })
})
</script>''' % post_body


@app.route('/more')
def load_post():
    return generate_lorem_ipsum(n=1)

# custom flask cli command
@app.cli.command()
def hello():
    """Just say hello."""
    click.echo('Hello, Human!')
