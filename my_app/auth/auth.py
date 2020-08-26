from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from sqlalchemy.exc import IntegrityError

from my_app import db
from my_app.auth.forms import SignupForm, LoginForm
from my_app.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    if form.validate_on_submit():
        '''
        name = form.first_name.data
        flash(f"Hello, {name}. You are signed up.")
        '''
        user = User(firstname=form.first_name.data, lastname=form.last_name.data, email=form.email.data)
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f"Hello, {user.firstname} {user.lastname}. You are signed up.")
        except IntegrityError:
            db.session.rollback()
            flash(f'Error, unable to register {form.email.data}. ', 'error')
            return redirect(url_for('auth.signup'))
        return redirect(url_for('main.index'))
    return render_template('signup.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        # Set the session cookie with a value for email address.
        session['name'] = request.form['email']
        return redirect(url_for('main.index', name=session['name']))
    return render_template('login.html', form=form)


@auth_bp.route('/logout')
def logout():
    # Demonstration of sessions. Remove the email from the session if it's there.
    session.pop('name', None)
    return redirect(url_for('main.index'))
