import logging
import email

from google.appengine.ext import webapp
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.ext.webapp.util import run_wsgi_app

from models import QuickLink


class AddQuickLink(InboundMailHandler):
    def receive(self, mail_message):
        if mail_message.sender != 'Agam Brahma <agam.brahma@gmail.com>':
            logging.error('Received email from an email address other than my own ?!')
            return

        text_bodies = list(mail_message.bodies('text/plain'))
        body = text_bodies[0]

        logging.debug("Received message from : " + mail_message.sender + ", to : " + mail_message.to + ", with subject: " + mail_message.subject + ", messsage is : " + body[1].decode())

        link = QuickLink(shortlink=mail_message.subject, longlink=body[1].decode())
        link.put()


application = webapp.WSGIApplication(
        [AddQuickLink.mapping()], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()

