#!/usr/bin/env python

"""main.py - This file contains handlers that are called by taskqueue and/or
cronjobs."""
import logging

import webapp2
from google.appengine.api import mail, app_identity
from api import HighNoon

from models import User


class UpdateAverageMovesRemaining(webapp2.RequestHandler):
    def post(self):
        """Update game listing announcement in memcache."""
        HighNoon._cache_average_attempts()
        self.response.set_status(204)


app = webapp2.WSGIApplication([
    ('/tasks/cache_average_attempts', UpdateAverageMovesRemaining),
], debug=True)
