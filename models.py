from google.appengine.ext import db

class PosterousPost(db.Model):
    """Models summary information about a Posterous post"""
    post_id = db.IntegerProperty()
    post_title = db.StringProperty()
    post_url = db.StringProperty()
    post_text = db.TextProperty()

    def to_dict(self):
        return dict([(p, unicode(getattr(self, p))) for p in self.properties()])

class BlogPost(db.Model):
    """Info about a post on my blog"""
    title = db.StringProperty(required=True)
    slug = db.StringProperty(required=True)
    body = db.TextProperty(required=True)
    published = db.DateTimeProperty(auto_now_add=True)

class QuickLink(db.Model):
    """A quicklink for personal use"""
    shortlink = db.StringProperty(required=True)
    longlink = db.StringProperty(required=True)

