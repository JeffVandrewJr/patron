from app.admin import bp
from app.admin.btcpair import pairing
from app.admin.forms import BTCCodeForm
from flask_login import login_required, current_user
from app.models import User
from flask import flash, redirect, render_template, url_for


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    if not hasattr(current_user, 'role'):
        return redirect(url_for('main.index'))
    elif current_user.role != 'admin':
        return redirect(url_for('main.index'))
    return render_template('admin/adminpanel.html')


@bp.route('/btcpay', methods=['GET', 'POST'])
@login_required
def btcpay():
    if not hasattr(current_user, 'role'):
        return redirect(url_for('main.index'))
    elif current_user.role != 'admin':
        return redirect(url_for('main.index'))
    form = BTCCodeForm()
    if form.validate_on_submit():
        pairing(code=form.code.data, host=form.host.data)
        flash('Pairing to BTCPay is complete.')
        return redirect(url_for('admin.index'))
    return render_template('admin/btcpay.html', form=form)


@bp.route('/export')
@login_required
def subscriber_export():
    if not hasattr(current_user, 'role'):
        return redirect(url_for('main.index'))
    elif current_user.role != 'admin':
        return redirect(url_for('main.index'))
    users = User.query.all()
    return render_template('admin/export.html', users=users)
