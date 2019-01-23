from app import blog_engine
from app.email import email_post
from flask_blogging_patron.signals import editor_post_saved

'''
Subscribes to editor_post_saved signal from Flask-Blogging.
Upon receiving the signal, it emails the post to all paid
subscribers unless the post is marked 'noemail.'
'''


@editor_post_saved.connect
def email_trigger(sender, engine, post_id, user, post):
    send_post = blog_engine.storage.get_post_by_id(post_id)
    for tag in send_post['tags']:
        email = True
        if tag.lower() == 'public' or tag.lower() == 'noemail':
            email = False
            break
    if email:
        email_post(send_post)
