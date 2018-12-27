from app.admin import bp
from app.admin.btcpair import pairing
from app.admin.forms import BTCCodeForm
from app.models import User
from flask import flash, redirect, render_template, url_for


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('admin/adminpanel.html')


@bp.route('/btcpay')
def btcpay():
    form = BTCCodeForm()
    if form.validate_on_submit():
        pairing(code=form.code.data, host=form.host.data)
        flash('Pairing to BTCPay is complete.')
        return redirect(url_for('admin.index'))
    return render_template('admin/btcpay.html', form=form)


@bp.route('/export')
def subscriber_export():
    users = User.query.all()
    return render_template('admin/export.html', users=users)
