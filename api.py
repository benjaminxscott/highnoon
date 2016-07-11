# -*- coding: utf-8 -*-`

# LATER - update apiary with docs

# LATER - build data structure for card deck using random.shuffle()
# LATER - implement logic in /play for choosing and manipulating hand

# LATER - handle if opponent is none, can set later by hitting /game/challenge/rival_id
# LATER - send notification if rival_id is set

# LATER - sanitize user input using bleach and profanityfilter

import logging
import endpoints
from protorpc import remote, messages
from google.appengine.api import memcache
from google.appengine.api import taskqueue

from models import Player, PlayerMessage, Game, GameMessage,GameOverMessage
from models import StringMessage
from utils import get_by_urlsafe, uniq_id

PLAYER_REQUEST = endpoints.ResourceContainer(PlayerMessage)
GAME_REQUEST = endpoints.ResourceContainer(GameMessage)
GAME_LOOKUP_REQUEST = endpoints.ResourceContainer(game_id=messages.StringField(1, required=True ) )

GAME_PLAY_REQUEST = endpoints.ResourceContainer(
            game_id=messages.StringField(1, required=True ),
            player_id=messages.StringField(2, required=True )
            )

@endpoints.api(name='aceofblades', version='v1')
class AceofBlades(remote.Service):
    """Game API"""
    @endpoints.method(request_message=PLAYER_REQUEST,
                      response_message=PlayerMessage,
                      path='player/new',
                      name='create_player',
                      http_method='POST' )
    def create_player(self, request):
        """Create a Player. Optionally set a (non)unique username"""
        
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
            
        # look up rival, if provided
        if request.rival_id is None:
            rival = None
        else:
            rival = Player.query(Player.player_id == request.rival_id).get()
            if rival is None:
                raise endpoints.BadRequestException('specified rival_id not found')
                
        # generate new game 
        game_id = uniq_id()
        game = Game(game_id = game_id, slinger = slinger.key, rival = rival.key)
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
                      response_message=GameOverMessage,
                      path='game/cancel/{game_id}',
                      name='cancel_game',
                      http_method='GET' )
    
    def cancel_game(self, request):
        """Remove an active game"""
        
        game = Game.query(Game.game_id == request.game_id).get()
        
        if game is None:
            raise endpoints.BadRequestException('specified game_id not found')
        
        if game.winner is not None:
            raise endpoints.ForbiddenException('that game is finished and cannot be modified')
            
        game.key.delete()
        
        return game.end_game(winner = None)
        
    @endpoints.method(request_message=GAME_PLAY_REQUEST,
                      response_message=GameOverMessage,
                      path='game/play/{game_id}/{player_id}',
                      name='play_game',
                      http_method='GET' )
                      
  # TODO - implement with post (put?)
                      
    def play_game(self, request):
        """Choose an action in the current game"""
        
        game = Game.query(Game.game_id == request.game_id).get()
        if game is None:
            raise endpoints.BadRequestException('specified game_id not found')
            
        if game.winner is not None:
            raise endpoints.ForbiddenException('that game is finished and cannot be modified')
            
        # check if player exists
        contender = Player.query(Player.player_id == request.player_id).get()
        
        if contender is None:
            raise endpoints.BadRequestException('specified player_id not found')
            
        # check if player is valid for this game
        if game.slinger == contender.key or game.rival == contender.key:
            winner = contender.key
        
        else:
            raise endpoints.UnauthorizedException('specified player_id not valid for this game')
        
        return game.end_game(winner)
        
                
# TODO - implement from boilerplate: get_high_scores / get_user_rankings / get_game_history
# TODO - add email cronjob

# --- RUN ---
api = endpoints.api_server([AceofBlades])