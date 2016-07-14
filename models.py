
import random
import json
from datetime import date
from protorpc import messages
from google.appengine.ext import ndb

# ASK: possible to use obj.key rather than storing explicit ID?
# ran into issue trying to query with just the int ID and not , although
# seemed cleaner to let the DB keep track of primary key and return
# obj.key.id()

# --- Request parameters ---


class PlayerMessage(messages.Message):
    """Used to create a new player"""
    desired_name = messages.StringField(1)
    email = messages.StringField(2)
    player_id = messages.StringField(3)
    player_name = messages.StringField(4)
    wins = messages.IntegerField(5)


class GameMessage(messages.Message):
    """Used to create and get information on games"""
    player_id = messages.StringField(1)
    game_id = messages.StringField(2)
    health = messages.IntegerField(3)
    won = messages.BooleanField(4)

    action = messages.StringField(5)
    hint = messages.StringField(6)


class GameListMessage(messages.Message):
    """ returns list of game IDs for a given player ID"""
    completed_games = messages.StringField(1, repeated=True)
    inprogress_games = messages.StringField(2, repeated=True)


class GameHistoryMessage(messages.Message):
    """ returns list of dictionaries for the actions on a given game ID """
    # note that this is a string due to there not being a JsonField object defined in Messages class
    # - this is OK since the field is returned as a json.dumps(), which ends up being a list of dictionaries that can be read with json.loads()
    # ref https://cloud.google.com/appengine/docs/python/tools/protorpc/messages/fieldclasses
    history = messages.StringField(1) 


class LeaderboardMessage(messages.Message):
    """ returns list of dictionaries for high scores of players """
    player_scores = messages.StringField(1, repeated = True)

# --- Data Model ---


class Player(ndb.Model):
    """User profile"""
    player_id = ndb.StringProperty(required=True)
    player_name = ndb.StringProperty(default=None)
    player_email = ndb.StringProperty(default=None)
    needs_taunted = ndb.BooleanProperty(default=False)
    wins = ndb.IntegerProperty(default=0)

    def to_message(self):
        return PlayerMessage(player_id=self.player_id,
                             player_name=self.player_name,
                             email=self.player_email,
                             wins=self.wins)


class History (ndb.Model):
    game = ndb.KeyProperty(required=True)
    history = ndb.JsonProperty(default=[])


class Game(ndb.Model):
    """Game object"""
    game_id = ndb.StringProperty(required=True)
    player_id = ndb.StringProperty(required=True)
    won = ndb.BooleanProperty(default=None)

    round_count = ndb.IntegerProperty(default=0)
    health = ndb.IntegerProperty(default=200)
    fun_quotient = ndb.IntegerProperty(default=9)
    highnoon = ndb.IntegerProperty(default=0)

    def get_history(self):
        moves = History.query(History.game == self.key).get()
        return GameHistoryMessage(history=json.dumps(moves.history))

    def to_message(self, hint=None, action=None):
        return GameMessage(
            game_id=self.game_id,
            player_id=self.player_id,
            won=self.won,
            health=self.health,
            hint=hint,
            action=action
        )
