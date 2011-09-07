import logging
import email

from google.appengine.ext import webapp
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.ext.webapp.util import run_wsgi_app

# Assumption: I am the only editor of my blog. As such, all emails have to be from my account. Also, since I will use gmail, the content will be html-enclosed (though markdown-formatted). Additionally, I can assume it will never be a multi-part MIME message.

class AddBlogPost(InboundMailHandler):
    def receive(self, mail_message):
        html_bodies = list(mail_message.bodies('text/html'))
        if len(html_bodies) > 1:
            logging.info("Weird -- received multi-part message!")
        body = html_bodies[0]

        logging.info("Received message from : " + mail_message.sender + ", messsage is : " + body[1].decode())

application = webapp.WSGIApplication(
        [(AddBlogPost.mapping())], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()

