from google.appengine.ext import db

class PosterousPost(db.Model):
    """Models summary information about a Posterous post"""
    post_id = db.IntegerProperty()
    post_title = db.StringProperty()
    post_url = db.StringProperty()
    post_text = db.TextProperty()

    def to_dict(self):
        return dict([(p, unicode(getattr(self, p))) for p in self.properties()])
