from app import blog_engine
from app.main import bp
from app.models import BTCPayClientStore
from flask import redirect, url_for, flash, render_template, request
from flask_blogging_patron import PostProcessor
from flask_blogging_patron.views import page_by_id_fetched,\
        page_by_id_processed
from flask_login import current_user, login_required
from ruamel.yaml import YAML
import sys
import traceback


@bp.route('/')
@bp.route('/index')
def index():
    try:
        posts = blog_engine.storage.get_posts(
            count=1,
            recent=True,
            tag='public'
        )
        temp_post = posts[0]
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        sys.stdout.flush()
        flash('This site has no homepage yet. \
              Please create one.', 'warning')
        if current_user.is_authenticated and current_user.role == 'admin':
            return redirect(url_for('blogging.editor'))
        else:
            return redirect(url_for('auth.register'))
    config = blog_engine.config
    post = blog_engine.storage.get_post_by_id(temp_post['post_id'])
    meta = {}
    meta['is_user_blogger'] = False
    if current_user.is_authenticated:
        if hasattr(current_user, 'role'):
            if current_user.role == 'admin':
                meta['is_user_blogger'] = True
    meta['post_id'] = temp_post['post_id']
    meta['slug'] = PostProcessor.create_slug(temp_post['title'])
    page_by_id_fetched.send(
        blog_engine.app,
        engine=blog_engine,
        post=post,
        meta=meta
    )
    blog_engine.process_post(post, render=True)
    page_by_id_processed.send(
        blog_engine.app,
        engine=blog_engine,
        post=post,
        meta=meta
    )
    return render_template(
        'main/homepage.html',
        post=post,
        config=config,
        meta=meta
    )


@bp.route('/support')
def support():
    yaml = YAML(typ='safe')
    with open('pricing.yaml') as f:
        levels = yaml.load(f)
    return render_template('main/support.html', levels=levels)


@bp.route('/createinvoice')
@login_required
def create_invoice():
    price = int(request.args.get('price'))
    level = request.args.get('name')
    btc_client = BTCPayClientStore.query.first().client
    if btc_client is None:
        return 'BTCPay has not been paired!', 501
    inv_data = btc_client.create_invoice({
        "price": price,
        "currency": "USD",
        "buyer": {
            "name": current_user.username,
            "email": current_user.email,
        },
        "orderId": level,
        "notificationURL": url_for('api.update_sub'),
        "redirectURL": url_for('main.index')
    })
    return redirect(inv_data['url'])
