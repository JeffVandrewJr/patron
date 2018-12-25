from flask import redirect, url_for
from flask_blogging import BloggingEngine
from flask_blogging.processor import PostProcessor
from flask_blogging.signals import blueprint_created, engine_initialised
from flask_blogging.views import page_by_id
from flask_fileupload import FlaskFileUpload
from flask_login import current_user
from flask_principal import Principal
import traceback
import sys


class ProtectedBloggingEngine(BloggingEngine):
    def init_app(self, app, storage=None, cache=None):
        """
        Initialize the engine.

        :param app: The app to use
        :type app: Object
        :param storage: The blog storage instance that implements the
        :type storage: Object
        :param cache: (Optional) A Flask-Cache object to enable caching
        :type cache: Object
         ``Storage`` class interface.
        """

        self.app = app
        self.config = self.app.config
        self.storage = storage or self.storage
        self.cache = cache or self.cache
        self._register_plugins(self.app, self.config)

        from flask_blogging.views import create_blueprint
        blog_app = create_blueprint(__name__, self)

        @blog_app.before_request
        def protect():
            if current_user.is_authenticated:
                return None
            try:
                posts = self.storage.get_posts(
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
        # external urls
        blueprint_created.send(self.app, engine=self, blueprint=blog_app)
        self.app.register_blueprint(
            blog_app, url_prefix=self.app.config.get(
                "PROTECTED_BLOGGING_URL_PREFIX"
            ))

        self.app.extensions["FLASK_BLOGGING_ENGINE"] = self  # duplicate
        self.app.extensions["blogging"] = self
        self.principal = Principal(self.app)
        engine_initialised.send(self.app, engine=self)

        if self.config.get("BLOGGING_ALLOW_FILEUPLOAD", True):
            self.ffu = self.file_upload or FlaskFileUpload(app)
