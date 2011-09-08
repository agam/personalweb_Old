import logging
import os
import simplejson

from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from models import BlogPost

#TODO(agam): Use memcache

class GetPost(webapp.RequestHandler):
    def get(self, slug):
        q = BlogPost.all()
        q.order('-published')
        q.filter('slug = ', slug)
        blog_results = q.fetch(1)
        if len(blog_results) == 1:
            path = os.path.join(os.path.dirname(__file__), 'templates', 'blog.html')
            template_values = { 'articles': blog_results }
            output = template.render(path, template_values)
            self.response.out.write(output)
        else:
            self.redirect("/404")


class MainPage(webapp.RequestHandler):
    def get(self):
        q = BlogPost.all()
        q.order('-published')
        blog_results = q.fetch(5)
        path = os.path.join(os.path.dirname(__file__), 'templates', 'blog.html')
        template_values = { 'articles': blog_results }
        output = template.render(path, template_values)
        self.response.out.write(output)

class Browse(webapp.RequestHandler):
    def get(self):
        self.response.out.write("Browse Coming soon")

class NotFoundHandler(webapp.RequestHandler):
    def get(self):
        self.redirect('/404')

application = webapp.WSGIApplication(
        [('/blog/article/([^/]+)', GetPost),
         ('/blog/main/?', MainPage),
         ('/blog/browse/?', Browse),
         ('/.*$', NotFoundHandler),
         ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
