# -*- coding: utf-8 -*-`


import logging
import endpoints
import random
from protorpc import remote, messages
from google.appengine.api import memcache
from google.appengine.api import taskqueue

from models import Player, Game
from models import PlayerMessage, GameMessage, GameLookupMessage, GamePlayMessage
from utils import get_by_urlsafe, uniq_id

PLAYER_REQUEST = endpoints.ResourceContainer(PlayerMessage)
GAME_REQUEST = endpoints.ResourceContainer(GameMessage)
GAME_LOOKUP_REQUEST = endpoints.ResourceContainer(GameLookupMessage)
GAME_PLAY_REQUEST = endpoints.ResourceContainer(GamePlayMessage)

@endpoints.api(name='highnoon', version='v1')
class AceofBlades(remote.Service):
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
        game = Game(game_id = game_id, slinger = slinger.key)
        game.put()
        
        return game.to_message()
                
    
    @endpoints.method(request_message=GAME_LOOKUP_REQUEST,
                      response_message=GameMessage,
                      path='game/status/{game_id}',
                      name='read_game',
                      http_method='GET' )
                      
# TODO - implement get_user_games with query in games/user/{player_id}

    def read_game(self, request):
        """Get info about current game"""
        
        game = Game.query(Game.game_id == request.game_id).get()
        if game is None:
            raise endpoints.BadRequestException('specified game_id not found')
            
        return game.to_message()
        
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
        
        return game.to_message()
        
    @endpoints.method(request_message=GAME_PLAY_REQUEST,
                      response_message=GameMessage,
                      path='game/play',
                      name='play_game',
                      http_method='POST' )
                      
    def play_game(self, request):
        """Choose an action in the current game"""
        
        game = Game.query(Game.game_id == request.game_id).get()
        if game is None:
            raise endpoints.BadRequestException('specified game_id not found')
            
        # handle if game status is finished
        if game.won is not None:
            raise endpoints.ForbiddenException('that game is finished')
            
        # check if player exists and is valid for this game
        contender = Player.query(Player.player_id == request.player_id).get()
        
        if contender is None:
            raise endpoints.BadRequestException('specified player_id not found')
            
        elif game.slinger is not contender.key:
            raise endpoints.UnauthorizedException('specified player_id not valid for this game')
            
        
        # --- game logic ---
        hints = [
            "McCree stares with accusing blue eyes, baring your soul",
            "McCree asks if Lady Luck has visited recently, flexing his gun hand",
            "McCree holds his cap against the blazing sun, checking his watch",
            "McCree chews on a piece of unidentified jerky, smirking through a ghastly grin",
            "McCree reloads his revolver with a flick of the wrist, preparing to send you to the clearing at the end of the path"
            ]
        hint = random.choice (hints)
        
        # roll a random action for mcree
            
        actions = ['retreat','pursue','showdown']
        botChoice = random.choice(actions)
        
        if request.action in actions:
            action = request.action
        else:
            raise endpoints.BadRequestException('that action is not a possible choice')
        
        if botChoice is "pursue" and action is "retreat" \
            or botChoice is "showdown" and action is "pursue" \
            or botChoice is "retreat" and action is "showdown":
                # increment ultie meter
                game.highnoon = game.highnoon + 35
                if game.highnoon >= 70:
                    hint = random.choice (hints)
                game.put()
        
        if action is "pursue" and botChoice is "retreat" \
            or action is "showdown" and botChoice is "pursue" \
            or action is "retreat" and botChoice is "showdown":
                # roll for damage
                game.health = game.health - random.randint(20,50)
                game.put()
            
        # check if mccree is dead
        if game.health <= 0: 
            game.end_game(has_won = True)
        
        # roll to see if high noon procs
        if game.highnoon >= 100 :
            if game.randint(0, fun_quotient) == 0: # 1/12 chance for first time, then 1/9 until guaranteed at fifth time
                # ITS HIGH NOON.gif
                game.end_game(has_won = False)
            else:
                game.fun_quotient = game.fun_quotient - 3 # make the game even more fun by increasing the odds of insta-death
                # reset ultie meter
                game.highnoon = 0
                game.put()
            
        return game.to_message(hint = hint)
                
# TODO - implement from boilerplate: get_high_scores / get_user_rankings / get_game_history
# TODO - add email cronjob with stupid meme

# --- RUN ---
api = endpoints.api_server([AceofBlades])