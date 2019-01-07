from app import db
from app.admin_utils import bp
from app.models import SquareClient
from flask import redirect, url_for, flash


@bp.route('/deletesquare')
def delete_square(self):
    square = SquareClient.query.first()
    if square is not None:
        db.session.delete(square)
        db.session.commit()
    flash('Square deactivated.')
    return redirect(url_for('admin.index'))
