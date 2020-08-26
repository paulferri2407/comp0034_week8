from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index(name=''):
    return render_template('index.html', title="Home page", name=name)
