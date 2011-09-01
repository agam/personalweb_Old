import logging
import os

# No need for webapp stuff here, this is going to be run as a cron job.

print 'Content-Type: text/plain'
print 'Fetching posterous data'

api_token = BouCofdeoIrIfbpzqiBfroAxfhIiJjxJGeyGgckqhpvazirtlfIzBeIunGfmeyewlCJgpIBjfCvenGjgjezxzfDmrAdbCGouEhcc

# Fetch the last 20 posts, then the 20 before that, and so on.
# Stop when we retrieve a post that has been retrieved before.



