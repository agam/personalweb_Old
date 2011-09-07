import logging
import os
import simplejson
from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from models import PosterousPost

class PosterousQuery(webapp.RequestHandler):
    def get(self):
        offset = 0
        if self.request.get("page"):
            offset = int(self.request.get("page")) * 20
        memcache_key = self.request.get("order") + str(offset)
        results = memcache.get(memcache_key)
        if results is not None:
            self.response.out.write(results)
            logging.debug("Scored a memcache hit for key: " + memcache_key)
            return
        else:
            posterous_query = PosterousPost.all()
            if self.request.get("order") == "front":
                posterous_query.order("-post_id")
            else:
                posterous_query.order("post_id")
            posterous_results = posterous_query.fetch(20, offset=offset)
            results = simplejson.dumps([p.to_dict() for p in posterous_results])
	    self.response.out.write(results)
            if not memcache.add(memcache_key, results, 3600):
                logging.error("Memcache insert failed for key :" + memcache_key)

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
