from app import admin
from app.admin_views.forms import BTCCodeForm
from app.utils import pairing
from flask_admin import BaseView, expose
from flask import flash, redirect, url_for


class BTCPayView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def btcpay(self):
        form = BTCCodeForm()
        if form.validate_on_submit():
            pairing(code=form.code.data, host=form.host.data)
            flash('Pairing to BTCPay is complete.')
            return redirect(url_for('admin.index'))
        return self.render('admin/btcpay.html', form=form)


admin.add_view(BTCPayView(name='BTCPay Setup', endpoint='btcpay'))
