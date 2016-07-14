#!/usr/bin/env python

"""main.py - This file contains handlers that are called by taskqueue and/or
cronjobs."""
import logging

import webapp2
from google.appengine.api import mail, app_identity
from api import HighNoon

from models import Player


class SendTauntEmail(webapp2.RequestHandler):
    """ Send a snarky email to reinforce that the player has lost to McCree"""

    def get(self):
        # find all players who have set an email and have recently lost

        # LATER - add query index to allow searching for non-null emails
        # ref https://cloud.google.com/appengine/docs/python/ndb/queries
        losers = Player.query(Player.needs_taunted == True)

        for loser in losers:
            if loser.player_email is None:
                continue

            name=loser.player_name
            email=loser.player_email

            if name is None:
                name=""

            subject="Hello {} ".format(name)

            body="It's HIGH NOON"
            body=body + '<hr />'
            body=body + '<img src = "http://img.ifcdn.com/images/8b3e2b0811fd853e566f1c06b54de1368dc8efb5faba84144f4839ed41e64cdc_1.jpg" alt="highnoon.gif" >'
            # This will send test emails, the arguments to send_mail are:
            # from, to, subject, body
            mail.send_mail('noreply@{}.appspotmail.com'.format(app_identity.get_application_id()),
                           email,
                           subject,
                           body)

            loser.needs_taunted=False

        # return success
        self.response.set_status(204)

app=webapp2.WSGIApplication(
    [
        ('/crons/send', SendTauntEmail)
    ])
