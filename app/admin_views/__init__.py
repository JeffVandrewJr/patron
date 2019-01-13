from app import admin, db
from app.admin_views.forms import BTCCodeForm, SquareSetupForm, \
        GAForm, EmailSetupForm, IssoForm
from app.models import User, Square, PriceLevel, ThirdPartyServices, \
        Email
from app.utils import pairing
from app.admin_utils import isso_config
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask import flash, redirect, url_for, current_app
from flask_login import current_user
from flask_mail import Mail


class LibrePatronBaseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and \
                current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))


class BTCPayView(LibrePatronBaseView):
    @expose('/', methods=['GET', 'POST'])
    def btcpay(self):
        form = BTCCodeForm()
        if form.validate_on_submit():
            pairing(code=form.code.data, host=form.host.data)
            flash('Pairing to BTCPay is complete.')
            return redirect(url_for('admin.index'))
        return self.render('admin/btcpay.html', form=form)


admin.add_view(BTCPayView(name='BTCPay Setup', endpoint='btcpay'))


class GAView(LibrePatronBaseView):
    @expose('/', methods=['GET', 'POST'])
    def ga(self):
        form = GAForm()
        if form.validate_on_submit():
            ga = ThirdPartyServices.query.filter_by(name='ga').first()
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
        return self.render('admin/ga.html', form=form)


admin.add_view(GAView(name='Google Analytics', endpoint='ga'))


class IssoView(LibrePatronBaseView):
    @expose('/', methods=['GET', 'POST'])
    def isso(self):
        if Email.query.first() is None:
            flash('You must set up email first.')
            return redirect(url_for('admin.email'))
        form = IssoForm()
        if form.validate_on_submit():
            isso = ThirdPartyServices.query.filter_by(name='isso').first()
            if isso is None:
                isso = ThirdPartyServices(
                    name='isso',
                    code=form.code.data,
                )
                db.session.add(isso)
            else:
                isso.code = form.code.data
            db.session.commit()
            current_app.config['COMMENTS'] = True
            isso_config()
            flash('User comments active.')
            return redirect(url_for('admin.index'))
        return self.render('admin/isso.html', form=form)


admin.add_view(IssoView(name='Isso Comments', endpoint='isso'))


class SquareView(LibrePatronBaseView):
    @expose('/', methods=['GET', 'POST'])
    def square(self):
        form = SquareSetupForm()
        if form.validate_on_submit():
            square = Square.query.first()
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
        return self.render('admin/square.html', form=form)


admin.add_view(SquareView(name='Square Setup', endpoint='square'))


class EmailView(LibrePatronBaseView):
    @expose('/', methods=['GET', 'POST'])
    def email(self):
        form = EmailSetupForm()
        if form.validate_on_submit():
            email = Email.query.first()
            if email is None:
                email = Email(
                    server=form.server.data,
                    port=form.port.data,
                    username=form.username.data,
                    password=form.password.data,
                    outgoing_email=form.outgoing_email.data,
                )
                db.session.add(email)
            else:
                email.server = form.server.data
                email.port = form.port.data
                email.username = form.username.data
                email.password = form.password.data
                email.outgoing_email = form.outgoing_email.data
            db.session.commit()
            current_app.config['ADMIN'] = email.outgoing_email
            current_app.config['MAIL_SERVER'] = email.server
            current_app.config['MAIL_PORT'] = email.port
            current_app.config['MAIL_USERNAME'] = email.username
            current_app.config['MAIL_PASSWORD'] = email.password
            mail = Mail()
            mail.init_app(current_app)
            flash('Email server info saved.')
            return redirect(url_for('admin.index'))
        return self.render('admin/email.html', form=form)


admin.add_view(EmailView(name='Email Setup', endpoint='email'))


class LibrePatronModelView(ModelView):
    can_export = True
    create_modal = True
    edit_modal = True

    def is_accessible(self):
        return current_user.is_authenticated and \
                current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))


class UserView(LibrePatronModelView):
    column_exclude_list = ['password_hash']
    column_searchable_list = ['username', 'email']


class PriceView(LibrePatronModelView):
    list_template = 'admin/custom_list.html'


admin.add_view(UserView(User, db.session, name='Manage Users'))
admin.add_view(PriceView(
    PriceLevel,
    db.session,
    name='Price Levels'
))
