import logging
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp_util import run_wsgi_app

class Posterous(webapp.RequestHandler):
    def get(self):
        pass

application = webapp.WSGIApplication(
        [('/posterous', Posterous),
            ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
