import logging
import os

from google.appengine.api import memcache
from google.appengine.ext import webapp
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
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
        #TODO(agam): Implement this
        pass

class  AddQuickLink(InboundMailHandler):
    def receive(self, mail_message):
        if mail_message.sender != 'Agam Brahma <agam.brahma@gmail.com>':
            logging.error('Received email from an email address other than my own ?!')
            return

        text_bodies = list(mail_message.bodies('text/plain'))
        if len(text_bodies) > 1:
            logging.info("Weird -- received multi-part message!")
        body = text_bodies[0]
        logging.info("%s: %s" % ('Message bodies', ''.join('msg %d: %s; ' % x for x in enumerate(text_bodies))))

        logging.debug("Received message from : " + mail_message.sender + ", to : " + mail_message.to + ", with subject: " + mail_message.subject + ", messsage is : " + body[1].decode())

        link = QuickLink(shortlink=mail_message.subject, longlink=body[1].decode())
        link.put()

application = webapp.WSGIApplication(
        [('/quicklink/([^/]+)', GetQuickLink),
            ('/.*$', ShowAllQuickLinks),
            AddQuickLink.mapping(),
            ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()

