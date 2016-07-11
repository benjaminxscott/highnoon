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
    """Used to create and get information on games"""
    player_id = messages.StringField(1, required=True)
    player_name = messages.StringField(2)
    game_id = messages.StringField(3)
    won = messages.BooleanField(4)
    
    action = messages.StringField (5)
    health = messages.IntegerField (6)

class GameLookupMessage(messages.Message):
    game_id=messages.StringField(1, required=True ) 
    
class GamePlayMessage(messages.Message):
    game_id=messages.StringField(1, required=True )
    player_id=messages.StringField(2, required=True )
    action=messages.StringField(3, required=True )
    
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
    won = ndb.BooleanProperty(default=None)
    
    health = ndb.IntegerProperty (default = 200)
    fun_quotient = ndb.IntegerProperty (default = 12)
    action = ndb.StringProperty (default = None)
    
    highnoon = ndb.IntegerProperty (default = 0)
    
    def to_message(self):
        return GameMessage(
              game_id = self.game_id, 
              player_id = Player.query(Player.key == self.slinger).get().player_id,
              player_name = Player.query(Player.key == self.slinger).get().player_name,
              won = self.won,
              action = self.action,
              health = self.health
              )
             
    def end_game(self, has_won):
        # False if AI wins, True otherwise
        self.won = has_won
        self.put()
        
        return self.to_message()
