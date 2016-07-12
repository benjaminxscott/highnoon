
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
    player_id = messages.StringField(1 )
    player_name = messages.StringField(2)
    game_id = messages.StringField(3)
    health = messages.IntegerField (4)
    won = messages.BooleanField(5)
    
    action = messages.StringField (6)
    hint = messages.StringField (7)

class GameListMessage(messages.Message):
    """ returns list of game IDs for a given player ID"""
    game_list = messages.StringField(1, repeated=True)

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
    player_id = ndb.StringProperty(required=True)
    won = ndb.BooleanProperty(default=None)
    
    health = ndb.IntegerProperty (default = 200)
    fun_quotient = ndb.IntegerProperty (default = 9)
    highnoon = ndb.IntegerProperty (default = 0)
    
    def to_message(self, hint=None, action=None):
        return GameMessage(
              game_id = self.game_id, 
              player_id = self.player_id,
              player_name = Player.query(Player.player_id == self.player_id).get().player_name,
              won = self.won,
              health = self.health,
              hint = hint,
              action = action
              )
             
    def end_game(self, has_won):
        # False if AI wins, True otherwise
        self.won = has_won
        self.put()
        
        return self.to_message()
