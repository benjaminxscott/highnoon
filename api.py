# -*- coding: utf-8 -*-`

import logging
import endpoints
from google.appengine.ext import ndb
import random
from protorpc import remote, messages
from google.appengine.api import memcache
from google.appengine.api import taskqueue

from models import Player,History, Game 
from models import GameMessage, GameHistoryMessage, GameListMessage, PlayerMessage
from utils import get_by_urlsafe, uniq_id


# TODO - implement from boilerplate: get_high_scores / get_user_rankings 

PLAYER_REQUEST = endpoints.ResourceContainer(PlayerMessage)
GAME_REQUEST = endpoints.ResourceContainer(GameMessage)
GAME_LOOKUP_REQUEST = endpoints.ResourceContainer(game_id=messages.StringField(1, required=True ) )
PLAYER_LOOKUP_REQUEST = endpoints.ResourceContainer(player_id=messages.StringField(1, required=True ) )

# ASK : weird issue where getting 'parameter is required' in gcloud (works on dev_appserver) even when it's provided in post data, so removed 'required' flag which likely causes weird bugs
GAME_PLAY_REQUEST = endpoints.ResourceContainer(
            game_id=messages.StringField(1, required = True),
            player_id=messages.StringField(2),
            action=messages.StringField(3)
            )

@endpoints.api(name='highnoon', version='v1')
class HighNoon(remote.Service):
    """Game API"""
    @endpoints.method(request_message=PLAYER_REQUEST,
                      response_message=PlayerMessage,
                      path='player/new',
                      name='create_player',
                      http_method='POST' )
    def create_player(self, request):
        """Create a Player. Optionally set a (non)unique username"""
        
        # LATER: include funny response when popular slinger names are chosen
        
        player_name = None
        if request.desired_name is not None:
            player_name = request.desired_name
            
        player_id = uniq_id()
        
        player = Player(player_id = player_id, player_name=player_name)
        player.put()
        
        return player.to_message()

    @endpoints.method(request_message=GAME_REQUEST,
                      response_message=GameMessage,
                      path='game/new',
                      name='create_game',
                      http_method='POST' )
    def create_game(self, request):
        """create a new game """
        
        # look up initiating player
        slinger = Player.query(Player.player_id == request.player_id).get()
        
        if slinger is None:
            raise endpoints.BadRequestException('specified player_id not found')
            
        # generate new game 
        game_id = uniq_id()
        game = Game(game_id = game_id, player_id = slinger.player_id)
        game.put()
        
        # create game history for this game
        history = History(game = game.key)
        history.put()
        
        return game.to_message()
                

    @endpoints.method(request_message=GAME_LOOKUP_REQUEST,
                      response_message=GameMessage,
                      path='game/status/{game_id}',
                      name='read_game',
                      http_method='GET' )
                      

    def read_game(self, request):
        """Get info about current game"""
        
        game = Game.query(Game.game_id == request.game_id).get()
        if game is None:
            raise endpoints.BadRequestException('specified game_id not found')
            
        return game.to_message()
        
    @endpoints.method(request_message=GAME_LOOKUP_REQUEST,
                      response_message=GameHistoryMessage,
                      path='game/history/{game_id}',
                      name='get_game_history',
                      http_method='GET' )
                      

    def get_game_history(self, request):
        """Get history for specified game"""
        
        game = Game.query(Game.game_id == request.game_id).get()
        if game is None:
            raise endpoints.BadRequestException('specified game_id not found')
            
        return game.get_history()
        
    @endpoints.method(request_message=PLAYER_LOOKUP_REQUEST,
                      response_message=GameListMessage,
                      path='game/list/{player_id}',
                      name='get_user_games',
                      http_method='GET' )
    
    def get_user_games(self, request):
        game_list = []
        # check if player exists and is valid for this game
        player = Player.query(Player.player_id == request.player_id).get()
        
        if player is None:
            raise endpoints.BadRequestException('specified player_id not found')
            
        # find all games where player ID is listed
        results = Game.query(Game.player_id == request.player_id)
        
        for game in results:
            game_list.append(game.game_id)
    
        return GameListMessage(game_list = game_list)
        
    @endpoints.method(request_message=GAME_LOOKUP_REQUEST,
                      response_message=GameMessage,
                      path='game/cancel/{game_id}',
                      name='cancel_game',
                      http_method='GET' )
    
    def cancel_game(self, request):
        """Remove an active game"""
        
        game = Game.query(Game.game_id == request.game_id).get()
        
        if game is None:
            raise endpoints.BadRequestException('specified game_id not found')
        
        if game.won is not None:
            raise endpoints.ForbiddenException('that game is finished and cannot be modified')
            
        game.key.delete()
        
        return GameMessage(game_id = game.game_id)
        
    @endpoints.method(request_message=GAME_PLAY_REQUEST,
                      response_message=GameMessage,
                      path='game/play',
                      name='play_game',
                      http_method='POST' )
                      
    def play_game(self, request):
        """Choose an action in the current game"""
        
        game = Game.query(Game.game_id == request.game_id).get()
        if game is None:
            raise endpoints.BadRequestException('specified game_id {} not found'.format(request.game_id))
            
        # handle if game status is finished
        if game.won is not None:
            raise endpoints.ForbiddenException('that game is finished')
            
        # check if player exists and is valid for this game
        contender = Player.query(Player.player_id == request.player_id).get()
        
        if contender is None:
            raise endpoints.BadRequestException('specified player_id not found')
            
        elif game.player_id != contender.player_id:
            raise endpoints.UnauthorizedException('specified player_id not valid for this game')
            
        
        # --- game logic ---
        hint = None
        hints = [
            "McCree stares with accusing blue eyes, baring your soul",
            "McCree asks if Lady Luck has visited recently, flexing his gun hand",
            "McCree holds his cap against the blazing sun, checking his watch",
            "McCree chews on a piece of unidentified jerky, smirking through a ghastly grin",
            "McCree reloads his revolver with a flick of the wrist, preparing to send you to the clearing at the end of the path"
            ]
        
        # roll a random action for mcree
            
        actions = ['retreat','pursue','showdown']
        botAction = random.choice(actions)
        
        if request.action in actions:
            action = request.action
        else:
            raise endpoints.BadRequestException('that action is not a possible choice')
        
        # increment round counter
        game.round_count = game.round_count + 1
        
        if (botAction == "pursue" and action == "retreat") \
            or (botAction == "showdown" and action == "pursue") \
            or (botAction == "retreat" and action == "showdown"):
                # McCree won the round, increment ultie meter
                game.highnoon = game.highnoon + 35
                if game.highnoon >= 70:
                    hint = random.choice (hints)
        
        if (action == "pursue" and botAction == "retreat") \
            or (action == "showdown" and botAction == "pursue") \
            or (action == "retreat" and botAction == "showdown"):
                # You won the round, roll for damage
                game.health = game.health - random.randint(20,30)
            
        else:
            # stalemate, which helps McCree a bit 
            game.highnoon = game.highnoon + 15
            
        # check if mccree is dead
        if game.health <= 0: 
            game.won = True
        
        # ultie meter is full - roll to see if high noon procs
        if game.highnoon >= 100 :
            if random.randint(0, game.fun_quotient) == 0: # 1/9 chance for first time, then 1/6 until guaranteed at fourth meter refill
                hint = "ITS HIGH NOON - a red mist fills your eyes"
                game.won = False
            else:
                # narrowly avoided certain demise
                hint = "Luckily you're behind cover when you hear ITS HIGH NOON"
                game.fun_quotient = game.fun_quotient - 3 # make the game even more fun by increasing the odds of insta-death
                # reset ultie meter
                game.highnoon = 0
            
        moves = History.query(History.game == game.key).get()
        
        # build dict of round outcomes
        action_dict = {
            "player_action": action,
            "ai_action": botAction,
            "health": game.health,
            "highnoon_meter": game.highnoon,
            "fun_quotient": game.fun_quotient,
            "won": game.won,
            "round_count": game.round_count
            
        }
        # append to history
        moves.history.append(action_dict)
        moves.put()
        
        game.put()
        # if game.won == None, we continue - else it's over
        return game.to_message(hint = hint, action = botAction)
        
# --- RUN ---
api = endpoints.api_server([HighNoon])