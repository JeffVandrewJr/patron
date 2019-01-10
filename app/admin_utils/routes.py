from app import db
from app.admin_utils import bp
from app.models import Square, ThirdPartyServices
from flask import redirect, url_for, flash, current_app


@bp.route('/deletesquare')
def delete_square():
    square = Square.query.first()
    if square is not None:
        db.session.delete(square)
        db.session.commit()
    flash('Square deactivated.')
    return redirect(url_for('admin.index'))


@bp.route('/deletega')
def delete_ga():
    ga = ThirdPartyServices.query.filter_by(
        name='ga').first()
    if ga is not None:
        db.session.delete(ga)
        db.session.commit()
    current_app.config['BLOGGING_GOOGLE_ANALYTICS'] = None
    flash('Google Analytics deactivated.')
    return redirect(url_for('admin.index'))
