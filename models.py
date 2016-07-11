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
    rival_id = messages.StringField(2, required=True)
    game_id = messages.StringField(3)

class GameOverMessage(messages.Message):
    """Used to create a new game"""
    game_id = messages.StringField(1)
    winner_id = messages.StringField(2)
    winner_name = messages.StringField(3)
    
# --- Data Model ---
class Player(ndb.Model):
    """User profile"""
    player_id = ndb.StringProperty(required=True)
    player_name =ndb.StringProperty()
    
    def to_message(self):
        return PlayerMessage(player_id=self.player_id, player_name= self.player_name)
       
       
class Hand(ndb.Model):
    # TODO implement
    
    cards = ndb.JsonProperty(required = True)
    has_ace = ndb.BooleanProperty(required = True, default=False)
    
class Game(ndb.Model):
    """Game object"""
    game_id = ndb.StringProperty(required=True)
    
    slinger = ndb.KeyProperty(required=True, kind='Player')
    
    # TODO - later make rival optional and visit URL to challenge them
    rival = ndb.KeyProperty(required=True,kind='Player', default=None)
    
    winner = ndb.KeyProperty(kind='Player', default=None)
    
    def to_message(self):
        return GameMessage(
              game_id = self.game_id, 
              player_id = Player.query(Player.key == self.slinger).get().player_id ,
              rival_id = Player.query(Player.key == self.rival).get().player_id 
              )
             
    def end_game(self, winner):
        # winner is a Player object
        self.winner = winner
        self.put()
        
        # if game was canceled before ending
        if self.winner is None:
            return GameOverMessage(
                game_id = self.game_id,
                winner_id = None,
                winner_name = None
                )
            
        else:
            return GameOverMessage(
                game_id = self.game_id,
                winner_id = Player.query(Player.key == self.winner).get().player_id ,
                winner_name = Player.query(Player.key == self.winner).get().player_name ,
                )

class StringMessage(messages.Message):
    """StringMessage-- outbound (single) string message"""
    message = messages.StringField(1, required=True)
