from app.blogging import bp
from datetime import datetime
from flask import flash, redirect, url_for
from flask_login import current_user


@bp.before_request
def protect():
    if current_user.is_authenticated:
        if datetime.today() <= current_user.expiration:
            return None
        else:
            flash('You must have a paid-up subscription \
                  to view updates.', 'warning')
            return redirect(url_for('auth.account'))
    else:
        flash('Please login to view updates.', 'warning')
        return redirect(url_for('auth.login'))
