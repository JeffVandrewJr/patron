from app import admin, db
from app.admin_views.forms import BTCCodeForm, SquareSetupForm, \
        GAForm, EmailSetupForm, IssoForm, ThemeForm
from app.models import User, Square, PriceLevel, ThirdPartyServices, \
        Email, BTCPayClientStore
from app.utils import pairing, hup_gunicorn
from app.admin_utils.utils import isso_config
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask import flash, redirect, url_for, current_app
from flask_login import current_user
from threading import Thread

'''
Flask-Admin creates views in the admin panel using classes.
These classes are loaded using the load_admin function.
This __init__ file is loaded in the app factory to register
the necessary classes to Flask-Admin.
'''


class LibrePatronBaseView(BaseView):
    # protects admin panel from regular users
    def is_accessible(self):
        return current_user.is_authenticated and \
                current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))


class BTCPayView(LibrePatronBaseView):
    @expose('/', methods=['GET', 'POST'])
    def btcpay(self):
        # custom view to pair BTCPay
        form = BTCCodeForm()
        btcpay = BTCPayClientStore.query.first()
        if form.validate_on_submit():
            try:
                pairing(code=form.code.data, host=form.host.data)
            except Exception as e:
                flash(f'Pairing failed. Error msg: {e}')
                current_app.logger.exception(e)
                return redirect(url_for('admin.index'))
            flash('Pairing to BTCPay is complete.')
            return redirect(url_for('admin.index'))
        return self.render('admin/btcpay.html', form=form, btcpay=btcpay)


admin.add_view(BTCPayView(name='BTCPay Setup', endpoint='btcpay'))


class GAView(LibrePatronBaseView):
    @expose('/', methods=['GET', 'POST'])
    def ga(self):
        # custom view to input Google Analytics UA code
        form = GAForm()
        ga = ThirdPartyServices.query.filter_by(name='ga').first()
        if form.validate_on_submit():
            if ga is None:
                ga = ThirdPartyServices(
                    name='ga',
                    code=form.code.data,
                )
                db.session.add(ga)
            else:
                ga.code = form.code.data
            db.session.commit()
            current_app.config['BLOGGING_GOOGLE_ANALYTICS'] = \
                ga.code
            flash('Google Analytics data saved.')
            return redirect(url_for('admin.index'))
        return self.render('admin/ga.html', form=form, ga=ga)


admin.add_view(GAView(name='Google Analytics', endpoint='ga'))


class ThemeView(LibrePatronBaseView):
    @expose('/', methods=['GET', 'POST'])
    def theme(self):
        # custom view to set theme
        form = ThemeForm()
        theme = ThirdPartyServices.query.filter_by(name='theme').first()
        if theme is None:
            temp_theme = current_app.config['THEME']
        else:
            temp_theme = theme.code
        if form.validate_on_submit():
            if theme is None:
                theme = ThirdPartyServices(
                    name='theme',
                    code=form.theme.data,
                )
                db.session.add(theme)
            else:
                theme.code = form.theme.data
            db.session.commit()
            current_app.config['THEME'] = form.theme.data
            current_app.jinja_env.cache = {}
            current_app.jinja_env.globals['THEME_FILE'] = 'themes/' + \
                form.theme.data + '.min.css'
            flash('Theme saved. Switch from the admin panel back to \
                    your site to see the changes. You may need to reload.')
            Thread(target=hup_gunicorn)
            return redirect(url_for('theme.theme'))
        return self.render(
                'admin/theme.html', form=form, current_theme=temp_theme)


admin.add_view(ThemeView(name='Set Theme', endpoint='theme'))


class IssoView(LibrePatronBaseView):
    @expose('/', methods=['GET', 'POST'])
    def isso(self):
        # custom view to activate isso comments
        if Email.query.first() is None:
            flash('You must set up email first.')
            return redirect(url_for('email.email'))
        elif Email.query.first().server is None:
            flash('You must set up email first.')
            return redirect(url_for('email.email'))
        form = IssoForm()
        isso = ThirdPartyServices.query.filter_by(name='isso').first()
        if form.validate_on_submit():
            if isso is None:
                isso = ThirdPartyServices(
                    name='isso',
                    code=form.code.data,
                )
                db.session.add(isso)
            else:
                isso.code = form.code.data
            db.session.commit()
            isso_config()
            current_app.config['COMMENTS'] = True
            flash('User comments active.')
            return redirect(url_for('admin.index'))
        return self.render('admin/isso.html', form=form, isso=isso)


admin.add_view(IssoView(name='Isso Comments', endpoint='isso'))


class SquareView(LibrePatronBaseView):
    @expose('/', methods=['GET', 'POST'])
    def square(self):
        # custom view to activate Square credit card pmts
        form = SquareSetupForm()
        square = Square.query.first()
        if form.validate_on_submit():
            if square is None:
                square = Square(
                    application_id=form.application_id.data,
                    location_id=form.location_id.data,
                    access_token=form.access_token.data,
                )
                db.session.add(square)
            else:
                square.application_id = form.application_id.data
                square.location_id = form.location_id.data
                square.access_token = form.access_token.data
            db.session.commit()
            flash('Square data saved.')
            return redirect(url_for('admin.index'))
        return self.render('admin/square.html', form=form, square=square)


admin.add_view(SquareView(name='Square Setup', endpoint='square'))


class EmailView(LibrePatronBaseView):
    @expose('/', methods=['GET', 'POST'])
    def email(self):
        # custom view to set SMTP settings
        form = EmailSetupForm()
        email = Email.query.first()
        if form.validate_on_submit():
            if email is None:
                email = Email(
                    server=form.server.data,
                    port=form.port.data,
                    username=form.username.data,
                    password=form.password.data,
                    default_sender=form.default_sender.data,
                    use_tls=True,
                )
                db.session.add(email)
            else:
                email.server = form.server.data
                email.port = form.port.data
                email.username = form.username.data
                email.default_sender = form.default_sender.data
                email.use_tls = True
            db.session.commit()
            flash('Email server info saved.')
            return redirect(url_for('email.email'))
        return self.render('admin/email.html', form=form, email=email)


admin.add_view(EmailView(name='Email Setup', endpoint='email'))


class LibrePatronModelView(ModelView):
    '''
    Inherits from the Flask-Admin ModelView, which is used for
    manually editing info in the database. This customizes the look
    for LibrePatron and also protects it from non-admins.
    '''
    can_export = True
    create_modal = True
    edit_modal = True

    def is_accessible(self):
        return current_user.is_authenticated and \
                current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))


class UserView(LibrePatronModelView):
    '''
    Allows admins to search for users by username or email. Also
    excludes password hashes from the table of users for aesthetic
    reasons.
    '''
    column_exclude_list = ['password_hash', 'renew']
    column_searchable_list = ['username', 'email']


class PriceView(LibrePatronModelView):
    '''
    This is a special version of ModelView for editing price levels
    stored in the database. The custom template warns the admin about
    the consequences of changing price levels.
    '''
    list_template = 'admin/custom_list.html'


admin.add_view(UserView(User, db.session, name='Manage Users'))
admin.add_view(PriceView(
    PriceLevel,
    db.session,
    name='Price Levels'
))
