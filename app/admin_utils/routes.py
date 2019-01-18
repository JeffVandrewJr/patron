from app import db
from app.admin_utils import bp
from app.email import send_email
from app.models import Square, ThirdPartyServices, User, Email
from flask import redirect, url_for, flash, current_app
from flask_login import current_user


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
    flash('''
          Comments deactivated. Due to browser caching,
           there can be a delay before comments disappear.
          ''')
    return redirect(url_for('admin.index'))


@bp.route('/testemail')
def test_email():
    email = Email.query.first()
    send_email(
        subject='Test Email',
        sender=email.default_sender,
        recipients=[current_user.email],
        text_body='Test Email.',
        html_body=None,
    )
    flash('Test email sent to administrator.')
    return redirect(url_for('admin.index'))
