from app import app
from app.blogging import bp
from app.blogging.forms import ModifiedBlogEditor
from datetime import datetime
from flask import flash, redirect, render_template, url_for, request
from flask_blogging.processor import PostProcessor
from flask_blogging.signals import editor_post_saved, editor_get_fetched
from flask_blogging.views import _clear_cache, _store_form_data
from flask_login import current_user, login_required
from flask_principal import PermissionDenied


@bp.before_request
def protect():
    if current_user.is_authenticated:
        if datetime.today() <= current_user.expiration:
            return None
        else:
            flash('You must have a paid-up subscription \
                  to view updates.')
            return redirect(url_for('auth.account'))
    else:
        flash('Please login to view updates.')
        return redirect(url_for('auth.login'))


@bp.route('/editor/', defaults={'post_id': None}, methods=['GET', 'POST'])
@bp.route('/editor/<post_id>', methods=['GET', 'POST'])
@login_required
def editor(post_id):
    blogging_engine = app.blog_engine
    cache = blogging_engine.cache
    if cache:
        _clear_cache(cache)
    try:
        with blogging_engine.blogger_permission.require():
            post_processor = blogging_engine.post_processor
            config = blogging_engine.config
            storage = blogging_engine.storage
            if request.method == 'POST':
                form = ModifiedBlogEditor(request.form)
                if form.validate():
                    post = storage.get_post_by_id(post_id)
                    if (post is not None) and \
                            (PostProcessor.is_author(post, current_user)) and \
                            (str(post["post_id"]) == post_id):
                        pass
                    else:
                        post = {}
                    escape_text = config.get("BLOGGING_ESCAPE_MARKDOWN", True)
                    pid = _store_form_data(form, storage, current_user, post,
                                           escape_text)
                    editor_post_saved.send(blogging_engine.app,
                                           engine=blogging_engine,
                                           post_id=pid,
                                           user=current_user,
                                           post=post)
                    flash("Blog posted successfully!", "info")
                    slug = post_processor.create_slug(form.title.data)
                    return redirect(url_for("blogging.page_by_id", post_id=pid,
                                            slug=slug))
                else:
                    flash("There were errors in blog submission", "warning")
                    return render_template("blogging/editor.html", form=form,
                                           post_id=post_id, config=config)
            else:
                if post_id is not None:
                    post = storage.get_post_by_id(post_id)
                    if (post is not None) and \
                            (PostProcessor.is_author(post, current_user)):
                        tags = ", ".join(post["tags"])
                        form = ModifiedBlogEditor(
                            title=post["title"],
                            text=post["text"],
                            tags=tags
                        )
                        editor_get_fetched.send(blogging_engine.app,
                                                engine=blogging_engine,
                                                post_id=post_id,
                                                form=form)
                        return render_template("blogging/editor.html",
                                               form=form, post_id=post_id,
                                               config=config)
                    else:
                        flash("You do not have the rights to edit this post",
                              "warning")
                        return redirect(url_for("blogging.index",
                                                post_id=None))

            form = ModifiedBlogEditor()
            return render_template("blogging/editor.html", form=form,
                                   post_id=post_id, config=config)
    except PermissionDenied:
        flash("You do not have permissions to create or edit posts", "warning")
        return redirect(url_for("blogging.index", post_id=None))
