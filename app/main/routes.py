from app import protected_blog_engine
from app.main import bp
from flask import redirect, url_for
from flask_blogging.processor import PostProcessor
from flask_blogging.views import page_by_id
from flask_login import current_user
import sys
import traceback


@bp.route('/')
@bp.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('blogging.index'))
    try:
        posts = protected_blog_engine.storage.get_posts(
            count=1,
            recent=True,
            tag='public'
        )
        post = posts[0]
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        sys.stdout.flush()
        if current_user.is_authenticated:
            return redirect(url_for('blogging.editor'))
        else:
            return redirect(url_for('auth.register'))
    response = page_by_id(
        post_id=post['post_id'],
        slug=PostProcessor.create_slug(post['title'])
    )
    return response
