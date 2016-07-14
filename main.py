#!/usr/bin/env python

"""main.py - This file contains handlers that are called by taskqueue and/or
cronjobs."""
import logging

import webapp2
from google.appengine.api import mail, app_identity
from google.appengine.ext import ndb
from api import HighNoon

from models import User

# TODO test to make sure this works
class SendTauntEmail(webapp2.RequestHandler):
    def get(self):
        # find all players who have lost recently
        # ref https://cloud.google.com/appengine/docs/python/ndb/queries
        losers = Player.query(ndb.AND (Player.needs_taunted = True)
            
        for loser in losers:
            # skip people with no email set
            # LATER - could optimize by adjusting the query above - tried an AND expression and got 'can't have keyword in expression' error
            if loser.player_email is None:
                continue
            
            name = loser.player_name
            email = loser.email
            
            if name is None:
                name = ""
                
            subject = "Hello {} ".format(name)
                
            body = "It's HIGH NOON"
            body = body + '<hr />'
            body = body + '<img src = "http://img.ifcdn.com/images/8b3e2b0811fd853e566f1c06b54de1368dc8efb5faba84144f4839ed41e64cdc_1.jpg" alt="highnoon.gif" >'
            # This will send test emails, the arguments to send_mail are:
            # from, to, subject, body
            mail.send_mail('noreply@{}.appspotmail.com'.format(app_identity.get_application_id()),
                           email,
                           subject,
                           body)
                           
            loser.needs_taunted = False
    

# TODO - is this needed?
class UpdateAverageMovesRemaining(webapp2.RequestHandler):
    def post(self):
        """Update game listing announcement in memcache."""
        HighNoon._cache_average_attempts()
        self.response.set_status(204)


app = webapp2.WSGIApplication([
    ('/crons/send', SendTauntEmail),
    ('/tasks/cache_average_attempts', UpdateAverageMovesRemaining),
], debug=True)