from app import protected_blog_engine
from app.main import bp
from flask import redirect, url_for, flash, render_template
from flask_blogging.processor import PostProcessor
from flask_blogging.views import page_by_id
from flask_login import current_user
import os
from ruamel.yaml import YAML
import sys
import traceback


@bp.route('/')
@bp.route('/index')
def index():
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
        flash('This site has no homepage yet. \
              Please create one.')
        if current_user.is_authenticated and current_user.role == 'admin':
            return redirect(url_for('blogging.editor'))
        else:
            return redirect(url_for('auth.register'))
    response = page_by_id(
        post_id=post['post_id'],
        slug=PostProcessor.create_slug(post['title'])
    )
    return response


@bp.route('/support')
def support():
    yaml = YAML(typ='safe')
    with open('pricing.yaml') as f:
        levels = yaml.load(f)
    return render_template('main/support.html', levels=levels)


@bp.route('/createinvoice')
def create_invoice():
    # TODO accepts URL ? arguments, passes those arguments to BTCPay
    # to prevent spam, check for user authentication
    # if unauthenticated, redirect to registration page
    return 'Not implemented'


@bp.route('/account')
def account():
    # TODO show expiration and payment link
    return 'To be implemented.'
