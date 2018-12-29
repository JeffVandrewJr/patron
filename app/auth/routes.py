from app import db
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm, AdminForm,\
        ResetPasswordForm, ResetPasswordRequestForm
from app.email import send_password_reset_email
from app.models import User
from app.utils import is_safe_url
from flask import redirect, url_for, render_template, flash, current_app,\
        request, abort
from flask_login import current_user, login_user, logout_user, login_required
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
        flash('Successful login.', 'info')
        login_user(user, remember=form.remember_me.data)
        next = request.args.get('next')
        if not is_safe_url(next):
            return abort(400)
        if user.role == 'admin':
            identity_changed.send(
                current_app._get_current_object(),
                identity=Identity(user.id)
            )
        return redirect(next or url_for('main.index'))
    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You are logged out.', 'info')
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
            expiration=expiration,
            mail_opt_out=False
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
            role='admin',
            mail_opt_out=False
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are now registered as the admin.', 'info')
        return redirect(url_for('auth.login'))
    return render_template(
        'auth/adminsetup.html',
        title='Register as Administrator',
        form=form
    )


@bp.route('/account')
@login_required
def account():
    if hasattr(current_user, 'role'):
        if current_user.role == 'admin':
            return redirect(url_for('admin.index'))
    if current_user.mail_opt_out is not False:
        opt_out = True
    else:
        opt_out = False
    if current_user.expiration.date() < date.today():
        expires = 'Expired'
    else:
        expires = current_user.expiration.date()
    return render_template(
        'auth/account.html',
        opt_out=opt_out,
        expires=expires
    )


@bp.route('/mailopt')
@login_required
def mail_opt():
    if hasattr(current_user, 'role'):
        if current_user.role == 'admin':
            return redirect(url_for('admin.index'))
    if current_user.mail_opt_out is not False:
        current_user.mail_opt_out = False
        flash('Succesfully opted in.', 'info')
    else:
        current_user.mail_opt_out = True
        flash('Succesfully opted out.', 'info')
    db.session.commit()
    return redirect(url_for('auth.account'))


@bp.route('/resetrequest', methods=['GET', 'POST'])
def reset_password_request():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
            flash(
                'Check your email for reset instructions.',
                'warning'
            )
        else:
            flash(
                'No user registered under that email address.',
                'warning'
            )
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        flash(
            'You must log out before resetting your password.',
            'warning'
        )
        return redirect(url_for('main.index'))
    user = User.verify_reset_password_token(token)
    if not user:
        flash('Invalid reset token.', 'warning')
        return redirect(url_for('main.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
