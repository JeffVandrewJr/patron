from app import blog_engine, db
from app.main import bp
from app.models import BTCPayClientStore, Square, PriceLevel
from flask import redirect, url_for, flash, render_template, request
from flask_blogging_patron import PostProcessor
from flask_blogging_patron.views import page_by_id_fetched,\
        page_by_id_processed
from flask_login import current_user, login_required
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
    # set default pricing if none exists
    if PriceLevel.query.all() == []:
        level_1 = PriceLevel(
            name='Patron',
            description="You're a patron!",
            price=10,
        )
        level_2 = PriceLevel(
            name='Cooler Patron',
            description="You're a cooler patron!",
            price=20,
        )
        level_3 = PriceLevel(
            name='Coolest Patron',
            description="You're the best!",
            price=60,
        )
        db.session.add(level_1)
        db.session.add(level_2)
        db.session.add(level_3)
        db.session.commit()
    price_levels = PriceLevel.query.all()
    price_levels.sort(key=lambda x: x.price, reverse=False)
    return render_template('main/support.html',
                           levels=price_levels)


@bp.route('/creditcard')
def credit_card():
    price = request.args.get('price')
    if price is None:
        flash('There was an error. Try again.')
        return redirect(url_for('main.support'))
    square = Square.query.first()
    if square is not None:
        return render_template(
            'main/creditcard.html',
            application_id=square.application_id,
            location_id=square.location_id,
            price=price,
        )
    else:
        return redirect(url_for('main.index'))


@bp.route('/createinvoice')
@login_required
def create_invoice():
    user_arg = request.args.get('username')
    if user_arg is not None:
        if user_arg != current_user.username:
            flash('You are logged in as a different user!\
                  Please log out first.', 'warning')
            return redirect(url_for('main.index'))
        else:
            current_plan = current_user.role
            if current_plan is not None:
                price_level = PriceLevel.query.filter_by(
                    name=current_plan).first()
                if price_level is None:
                    return redirect(url_for('main.support'))
                else:
                    plan = price_level.name
                    price = price_level.price
            else:
                return redirect(url_for('main.support'))
    else:
        string_price = request.args.get('price')
        if string_price is None:
            return redirect(url_for('main.support'))
        plan = request.args.get('name')
        price = int(string_price)
        compare = PriceLevel.query.filter_by(price=price).first()
        if compare is None:
            return redirect(url_for('main.support'))
        elif compare.name != plan:
            return redirect(url_for('main.support'))
    btc_client_store = BTCPayClientStore.query.first()
    if btc_client_store is None:
        return 'BTCPay has not been paired!', 501
    elif btc_client_store.client is None:
        return 'BTCPay has not been paired!', 501
    else:
        btc_client = btc_client_store.client
        inv_data = btc_client.create_invoice({
            "price": price,
            "currency": "USD",
            "buyer": {
                "name": current_user.username,
                "email": current_user.email,
            },
            "orderId": plan,
            "extendedNotifications": True,
            "fullNotifications": True,
            "notificationURL": url_for(
                'api.update_sub',
                _external=True,
                _scheme='https'
            ),
            "redirectURL": url_for(
                'main.index',
                _external=True,
                _scheme='https'
            )
        })
        return redirect(inv_data['url'])
