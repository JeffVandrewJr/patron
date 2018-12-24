from app import protected_blog_engine
from app.main import bp
from flask import redirect, url_for, render_template
from flask_login import current_user
import sys
import traceback


@bp.route('/')
@bp.route('/index')
def index():
    posts = protected_blog_engine.storage.get_posts(
        count=1,
        recent=True,
        tag='public'
    )
    try:
        post = posts[0]
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        sys.stdout.flush()
        if current_user.is_authenticated:
            return redirect(url_for('blogging.editor'))
        else:
            return redirect(url_for('auth.register'))
    if not current_user.is_authenticated:
        return render_template(
            'blogging/page.html',
            post=post,
            config=protected_blog_engine.config
        )
    else:
        return redirect(url_for('blogging.index'))
