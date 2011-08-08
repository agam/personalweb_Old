from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class NotFoundPage(webapp.RequestHandler):
    def get(self):
	self.response.out.write("""
	<h3>You asked for a page - I can't give it to you</h3>
	""")

application = webapp.WSGIApplication(
	[(r'.*', NotFoundPage)], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
