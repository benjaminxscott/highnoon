"""models.py - This file contains the class definitions for the Datastore
entities used by the Game. Because these classes are also regular Python
classes they can include methods (such as 'to_form' and 'new_game')."""

import random
from datetime import date
from protorpc import messages
from google.appengine.ext import ndb

# ASK: possible to use obj.key rather than storing explicit ID? 
# ran into issue trying to query with just the int ID and not , although seemed cleaner to let the DB keep track of primary key and return obj.key.id() 

# --- Request parameters ---
class PlayerMessage(messages.Message):
    """Used to create a new player"""
    desired_name = messages.StringField(1)
    player_id = messages.StringField(2)
    player_name = messages.StringField(3)
    
class GameMessage(messages.Message):
    """Used to create a new game"""
    player_id = messages.StringField(1, required=True)
    rival_id = messages.StringField(2)
    game_id = messages.StringField(3)
    status = messages.StringField(4)

# --- Data Model ---
class Player(ndb.Model):
    """User profile"""
    player_id = ndb.StringProperty(required=True)
    player_name =ndb.StringProperty()
    
    def to_message(self):
        return PlayerMessage(player_id=self.player_id, player_name= self.player_name)
       
class Game(ndb.Model):
    """Game object"""
    game_id = ndb.StringProperty(required=True)
    slinger = ndb.KeyProperty(required=True, kind='Player')
    status = ndb.StringProperty(required=True, default="waiting")
    rival = ndb.KeyProperty(kind='Player', default=None)
    
    def to_message(self):
        return GameMessage(
          game_id = self.game_id, 
        # slinger is primary key into Player DB
          player_id = Player.query(Player.key == self.slinger).get().player_id ,
#TODO          rival_id = Player.query(Player.key == self.rival).get().player_id ,
          status = self.status)

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
