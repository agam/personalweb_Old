import logging
import os
import simplejson
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from models import PosterousPost

# TODO(agam): use memcache

class PosterousQueryFront(webapp.RequestHandler):
    def get(self):
        posterous_query = PosterousPost.all()
        if self.request.get("postid"):
            posterous_query.filter("post_id < " + str(self.request.get("postid")))
            logging.debug("Filtering by " + post_id)
        posterous_query.order("-post_id")
        posterous_results = posterous_query.fetch(20)
#        self.response.out.write('Content-Type: application/json')
	self.response.out.write(simplejson.dumps([p.to_dict() for p in posterous_results]))

class PosterousQueryBack(webapp.RequestHandler):
    def get(self):
        posterous_query = PosterousPost.all()
        if self.request.get("postid"):
            posterous_query.filter("post_id > " + str(self.request.get("postid")))
            logging.debug("Filtering by " + post_id)
        posterous_query.order("post_id")
        posterous_results = posterous_query.fetch(20)
#        self.response.out.write('Content-Type: application/json')
	self.response.out.write(simplejson.dumps([p.to_dict() for p in posterous_results]))


application = webapp.WSGIApplication(
        [('/posterous/getpagefront', PosterousQueryFront),
            ('/posterous/getpageback', PosterousQueryBack),
            ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
