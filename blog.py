import logging
import os
import simplejson

from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from models import BlogPost


class GetPost(webapp.RequestHandler):
    def get(self, slug): 
        path = os.path.join(os.path.dirname(__file__), 'templates', 'blog.html')
        memcache_result = memcache.get(slug)
        if memcache_result is not None:
            logging.info('Serving article from cache: %s' % slug)
            template_values = {
                    'single_post': True,
                    'articles': memcache_result
                    }
            output = template.render(path, template_values)
            self.response.out.write(output)
        else:
            q = BlogPost.all()
            q.filter('slug = ', slug)
            blog_results = q.fetch(1)
            if len(blog_results) == 1:
                template_values = { 
                        'single_post': True,
                        'articles': blog_results }
                output = template.render(path, template_values)
                self.response.out.write(output)
                # Individual articles NEVER change - so let them persist for a day
                memcache.add(slug, blog_results, 86400)
            else:
                self.redirect("/404")

class MainPage(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates', 'blog.html')
        template_values = {}

        memcache_result = memcache.get("mainpage")
        if memcache_result is not None:
            logging.info('Serving blog main page from cache')
            template_values = { 'articles': memcache_result }
        else:
            q = BlogPost.all()
            q.order('-published')
            blog_results = q.fetch(5)
            template_values = { 'articles': blog_results }
            # The blog's main page is cached for two minutes
            logging.info("Added main page to cache")
            memcache.add("mainpage", blog_results, 120)

        output = template.render(path, template_values)
        self.response.out.write(output)

# Next/Prev is lame -- come up with some other way of showing "everything
# other than the last five" items.
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
