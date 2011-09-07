import logging
import simplejson

from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from models import BlogPost

#TODO(agam): Use memcache

class GetPost(webapp.RequestHandler):
    def get(self):
        self.response.out.write("Posts Coming soon")

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.out.write("Main Coming soon")

class Browse(webapp.RequestHandler):
    def get(self):
        self.response.out.write("Browse Coming soon")


application = webapp.WSGIApplication(
        [('/blog/post/.*', GetPost),
         ('/blog/main/', MainPage),
         ('/blog/browse/', Browse),
         ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
