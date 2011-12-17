import logging
import os

from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from models import QuickLink

class GetQuickLink(webapp.RequestHandler):
    def get(self, link):
        memcache_result = memcache.get(link)
        if memcache_result is not None:
            # We have the url we need
            logging.info('Serving link from cache: %s->%s' % (link, memcache_result.longlink))
            self.redirect(memcache_result.longlink)
        else:
            logging.info('Did not find [%s] in memcache' % link)
            q = QuickLink.all()
            q.filter('shortlink = ', link)
            link_results = q.fetch(1)
            if len(link_results) == 1:
                logging.info('Serving link from datastore: %s->%s' % (link, link_results[0].longlink))
                memcache.add(link, link_results[0], 86400)
                self.redirect(link_results[0].longlink)
            else:
                logging.info('Quicklink not found! [%s]' % link)
                self.redirect('/404')

class ShowAllQuickLinks(webapp.RequestHandler):
    def get(self):
        pass

application = webapp.WSGIApplication(
        [('/quicklink/([^/]+)', GetQuickLink),
         ('/.*$', ShowAllQuickLinks),
         ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
