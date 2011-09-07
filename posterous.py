import logging
import os
import simplejson
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from models import PosterousPost

# TODO(agam): use memcache

class PosterousQuery(webapp.RequestHandler):
    def get(self):
        posterous_query = PosterousPost.all()
        offset = 0
        if self.request.get("order") == "front":
            posterous_query.order("-post_id")
        else:
            posterous_query.order("post_id")
        if self.request.get("page"):
            offset = int(self.request.get("page")) * 20
        posterous_results = posterous_query.fetch(20, offset=offset)
	self.response.out.write(simplejson.dumps([p.to_dict() for p in posterous_results]))

def query_counter(q, cursor=None, limit=1000):
    if cursor:
        q.with_cursor (cursor)
    count = q.count (limit=limit)
    if count == limit:
        return count + query_counter (q, q.cursor (), limit=limit)
    return count


class PosterousCount(webapp.RequestHandler):
    def get(self):
        posterous_query = PosterousPost.all();
        posterous_result = query_counter(posterous_query)
        self.response.out.write(simplejson.dumps({"count": posterous_result}))


application = webapp.WSGIApplication(
        [('/posterous/getposts', PosterousQuery),
         ('/posterous/getcount', PosterousCount),
            ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
