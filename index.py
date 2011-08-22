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

# Map urls
application = webapp.WSGIApplication(
	[('/', MainPage),
	 ('/index.html', MainPage),
	], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
