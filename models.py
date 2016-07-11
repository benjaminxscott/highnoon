"""models.py - This file contains the class definitions for the Datastore
entities used by the Game. Because these classes are also regular Python
classes they can include methods (such as 'to_form' and 'new_game')."""

import random
from datetime import date
from protorpc import messages
from google.appengine.ext import ndb

# --- Request parameters ---
class PlayerMessage(messages.Message):
    """Used to create a new player"""
    desired_name = messages.StringField(1)
    
class GameMessage(messages.Message):
    """Used to create a new game"""
    player_id = messages.StringField(1, required=True)
    rival_id = messages.StringField(2)

# --- Data Model ---
class Player(ndb.Model):
    """User profile"""
    player_id = ndb.StringProperty(required=True)
    player_name =ndb.StringProperty()

class Game(ndb.Model):
    """Game object"""
    game_id = ndb.StringProperty(required=True)
    slinger = ndb.KeyProperty(required=True, kind='Player')
    rival = ndb.KeyProperty(kind='Player', default=None)
    status = ndb.StringProperty(required=True, default="waiting")

    @classmethod

    def end_game(self, winner):
        # TODO called at end of hand processing logic
        # TODO - set winner ID
        self.status = "done"
        self.put()
        return True


class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)
