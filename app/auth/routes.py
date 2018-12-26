from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, AdminForm
from app.models import User
from flask import redirect, url_for, render_template, flash, current_app
from flask_login import current_user, login_user, logout_user
from flask_principal import Identity, identity_changed
from datetime import date, timedelta


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.account'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        if user.role == 'admin':
            identity_changed.send(
                current_app._get_current_object(),
                identity=Identity(user.id)
            )
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already registered.')
        return redirect(url_for('main.index'))
    elif User.query.filter_by(role='admin').first() is None:
        return redirect(url_for('auth.adminsetup'))
    form = RegistrationForm()
    if form.validate_on_submit():
        expiration = date.today() - timedelta(days=1)
        user = User(
            username=form.username.data,
            email=form.email.data,
            expiration=expiration
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now a registered user.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)


@bp.route('/adminsetup', methods=['GET', 'POST'])
def adminsetup():
    if User.query.filter_by(role='admin').first() is not None:
        flash('Administrator is already set.')
        return redirect(url_for('main.index'))
    form = AdminForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            expiration=date.max,
            role='admin'
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now registered as the admin.')
        return redirect(url_for('auth.login'))
    return render_template(
        'auth/adminsetup.html',
        title='Register as Administrator',
        form=form
    )


@bp.route('/account')
def account():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return render_template('auth/account.html')


@bp.route('/reset', methods=['GET', 'POST'])
def reset_password():
    # TODO insert password reset function
    return 'Not yet implemented.'
