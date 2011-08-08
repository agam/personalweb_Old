import logging
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

#TODO(agam): use webapp2

class MainPage(webapp.RequestHandler):
    def get(self):
	path = os.path.join(os.path.dirname(__file__), 'templates', 'index.html')
	template_values = {}
	output = template.render(path, template_values)
	self.response.out.write(output)

class AboutPage(webapp.RequestHandler):
    def get(self):
	path = os.path.join(os.path.dirname(__file__), 'templates', 'about.html')
	f = open(path, 'r')
	self.response.out.write(f.read())

# Map urls
application = webapp.WSGIApplication(
	[('/', MainPage),
	 ('/main/home', MainPage),
	 ('/main/about', AboutPage)
	], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
