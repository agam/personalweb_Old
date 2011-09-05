import logging
import os
import simplejson
import urllib
from google.appengine.api import urlfetch

from models import PosterousPost

# No need for webapp stuff here, this is going to be run as a cron job.

print 'Content-Type: text/plain'
print 'Fetching posterous data'

api_token = 'BouCofdeoIrIfbpzqiBfroAxfhIiJjxJGeyGgckqhpvazirtlfIzBeIunGfmeyewlCJgpIBjfCvenGjgjezxzfDmrAdbCGouEhcc'

# Fetch the last 20 posts, then the 20 before that, and so on.
# Stop when we retrieve a post that has been retrieved before.

page = 1
fetch_url_base = 'http://posterous.com/api/2/sites/1537630/posts/public?api_token=' + api_token

get_more_posts = True

while get_more_posts:
    fetch_url = fetch_url_base + '&page=' + str(page)
    result = urlfetch.fetch(fetch_url, deadline=600) # Cron jobs can take up to 10 minutes to time out
    if result.status_code == 200:
        try:
            posterous_response = simplejson.loads(result.content)
        except UnicodeDecodeError:
            try:
                logging.debug('Received non-utf8 response')
                posterous_response = simplejson.loads(result.content, encoding='latin-1')
            except UnicodeDecodeError:
                logging.debug('Received non-utf8/non-latin1 response ... giving up')
                break

        if len(posterous_response) == 0:
            get_more_posts = False
            break

        for post in posterous_response:
            logging.debug('Received a new post with id = ' + str(post["id"]))    
            newpost = PosterousPost.get_or_insert(str(post["id"]))
            if newpost.post_title:
                # We reached a post we already have, end the retreive process
                logging.debug('Found pre-existing post with title: ' + newpost.post_title)
                get_more_posts = False
                break

            newpost = PosterousPost(key_name = str(post["id"]),
                    post_id = post["id"],
                    post_title = post["title"],
                    post_url = post["full_url"],
                    post_text = post["body_full"])
            newpost.post_title = post["title"]
            newpost.post_url = post["full_url"]
            newpost.post_text = post["body_full"]
            logging.debug('Added a new post : ' + str(newpost.post_id) + ',' + newpost.post_title)
            newpost.put()
        page = page + 1

    else:
        print 'Error: got status code %d while attempting to get new posterous posts!' % (result.status_code)
        get_more_posts = False

print 'Retreival process complete!'
