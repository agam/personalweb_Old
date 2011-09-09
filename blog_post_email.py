import email
import logging
import re
import unicodedata

from google.appengine.ext import webapp
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.ext.webapp.util import run_wsgi_app

from models import BlogPost

# Assumption: I am the only editor of my blog. As such, all emails have to be from my account. Also, since I will use gmail, the content will be html-enclosed (though markdown-formatted). Additionally, I can assume it will never be a multi-part MIME message.

def CreateSlug(title):
    # Inspired by 'slugify' in https://code.djangoproject.com/browser/django/trunk/django/template/defaultfilters.py
    MAX_SLUG_LENGTH = 50
    slug = unicodedata.normalize('NFKD', unicode(title)).encode('ascii', 'ignore')
    slug = unicode(re.sub('[^\w\s-]', '', slug).strip().lower())
    return re.sub('[-\s]+', '-', slug)


class AddBlogPost(InboundMailHandler):
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

        blogpost = BlogPost(title=mail_message.subject,
                slug=CreateSlug(mail_message.subject),
                body = body[1].decode())
        blogpost.put()

application = webapp.WSGIApplication(
        [(AddBlogPost.mapping())], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()

