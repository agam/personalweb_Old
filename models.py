from google.appengine.ext import db

class PosterousPost(db.Model):
    """Models summary information about a Posterous post"""
    post_title = db.StringProperty()
    post_url = db.StringProperty()
    post_text = db.TextProperty()
