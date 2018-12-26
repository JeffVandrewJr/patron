from datetime import date
from flask import redirect, url_for, flash
from flask_blogging import BloggingEngine
from flask_blogging.signals import blueprint_created, engine_initialised
from flask_fileupload import FlaskFileUpload
from flask_login import current_user
from flask_principal import Principal


class ProtectedBloggingEngine(BloggingEngine):
    def init_app(self, app, storage=None, cache=None):
        # extension of flask_blogging to allow protected posts
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
                if date.today() <= current_user.expiration:
                    return None
                else:
                    flash('You must have a paid-up subscription \
                          to view updates.')
                    redirect(url_for('main.account'))
            else:
                flash('Please login to view updates.')
                return redirect(url_for('auth.login'))
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
