import logging
import os
import simplejson
from google.appengine.api import urlfetch

from models import PosterousPost

# No need for webapp stuff here, this is going to be run as a cron job.

print 'Content-Type: text/plain'
print 'Fetching posterous data'

api_token = 'BouCofdeoIrIfbpzqiBfroAxfhIiJjxJGeyGgckqhpvazirtlfIzBeIunGfmeyewlCJgpIBjfCvenGjgjezxzfDmrAdbCGouEhcc'

# Fetch the last 20 posts, then the 20 before that, and so on.
# Stop when we retrieve a post that has been retrieved before.

fetch_url = 'http://posterous.com/api/2/sites/1537630/posts/public?api_token=' + api_token
page = 1

get_more_posts = True

while get_more_posts:
    payload = 'page=%d' % (page)
    logging.info('Retreiving posts with payload :' + payload)
    result = urlfetch.fetch(fetch_url, deadline=60)
    if result.status_code == 200:
        posterous_response = simplejson.loads(result.content)
        if len(posterous_response) == 0:
            get_more_posts = False
            break

        for post in posterous_response:
            newpost = PosterousPost.get_or_insert(str(post["id"]))
            if newpost.post_title:
                # We reached a post we already have, end the retreive process
                get_more_posts = False
                break

            newpost = PosterousPost(post_title = post["title"], post_url = post["full_url"], post_text = post["body_full"])
            newpost.post_title = post["title"]
            newpost.post_url = post["full_url"]
            newpost.post_text = post["body_full"]
            logging.info('Added a new post : ' + newpost.post_title)
            newpost.put()
    else:
        print 'Error: got status code %d while attempting to get new posterous posts!' % (result.status_code)
    page = page + 1

print 'Retreival process complete!'
