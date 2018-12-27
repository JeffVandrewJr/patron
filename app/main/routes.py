from app import blog_engine
from app.main import bp
from app.models import BTCPayClientStore
from flask import redirect, url_for, flash, render_template, request
from flask_blogging import PostProcessor
from flask_blogging.views import page_by_id
from flask_login import current_user
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
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    price = int(request.args.get('price'))
    level = request.args.get('name')
    btc_client = BTCPayClientStore.query.all().first()
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
