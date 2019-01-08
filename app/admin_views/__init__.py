from app import admin, db
from app.admin_views.forms import BTCCodeForm, SquareSetupForm
from app.models import User, Square
from app.utils import pairing
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask import flash, redirect, url_for
from flask_login import current_user


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
                )
                db.session.add(square)
            else:
                square.application_id = form.application_id.data
                square.location_id = form.location_id.data
            db.session.commit()
            flash('Square data saved.')
            return redirect(url_for('admin.index'))
        return self.render('admin/square.html', form=form)


admin.add_view(SquareView(name='Square Setup', endpoint='square'))


class LibrePatronModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and \
                current_user.role == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login'))


admin.add_view(LibrePatronModelView(User, db.session))
