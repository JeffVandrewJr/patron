from app import db
from app.admin_utils import bp
from app.models import Square, ThirdPartyServices, User
from flask import redirect, url_for, flash, current_app


@bp.route('/deletesquare')
def delete_square():
    square = Square.query.first()
    if square is not None:
        db.session.delete(square)
    cc_users = User.query.filter(User.square_id != None).all()
    for cc_user in cc_users:
        cc_user.square_id = None
        cc_user.square_card = None
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


@bp.route('/deactivateisso')
def deactivate_isso():
    isso = ThirdPartyServices.query.filter_by(
        name='isso').first()
    if isso is not None:
        db.session.delete(isso)
        db.session.commit()
    current_app.config['COMMENTS'] = False
    flash('Comments deactivated.')
    return redirect(url_for('admin.index'))
