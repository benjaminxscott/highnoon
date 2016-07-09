# -*- coding: utf-8 -*-`

import logging
import endpoints
from protorpc import remote, messages
from google.appengine.api import memcache
from google.appengine.api import taskqueue

from models import Player, PlayerMessage, Game, GameMessage
from models import StringMessage
from utils import get_by_urlsafe, uniq_id

import bleach
from profanity import contains_profanity

USER_REQUEST = endpoints.ResourceContainer(PlayerMessage)
GAME_REQUEST = endpoints.ResourceContainer(GameMessage)
GAME_LOOKUP_REQUEST = endpoints.ResourceContainer(game_id=messages.StringField(1, required=True ) )

@endpoints.api(name='aceofblades', version='v1')
class AceofBlades(remote.Service):
    """Game API"""
    @endpoints.method(request_message=USER_REQUEST,
                      response_message=StringMessage,
                      path='user',
                      name='create_user',
                      http_method='POST' )
    def create_user(self, request):
        """Create a Player. Optionally set a (non)unique username"""
        
        if contains_profanity(request.desired_name):
            raise endpoints.BadRequestException(
                    'player_name was not valid - perhaps it contained profanity')
        
        player_name = None
        if request.desired_name is not None:
            # DBG player_name = str(bleach.clean(request.desired_name))
            player_name = request.desired_name
            
        player_id = uniq_id()
        
        user = Player(player_id = player_id, player_name=player_name)
        user.put()
        
        # TODO return id and name as json instead
        return StringMessage(message='Player {} with ID {} has stepped through the door'.format(
                player_name, player_id))

# TODO /new game which finds use given player id and sets response to player in game object

    @endpoints.method(request_message=GAME_REQUEST,
                      response_message=StringMessage,
                      path='game',
                      name='create_game',
                      http_method='POST' )
    def create_game(self, request):
        """create a new game """
        
        # look up initiating player
        slinger = Player.query(Player.player_id == request.player_id).get()
        
        # generate new game 
        game_id = uniq_id()
        game = Game(game_id = game_id, slinger = slinger.key)
        
        return StringMessage(message='Game with ID {} for player ID {} and player name {} '.format(
                game_id, slinger.player_id, slinger.player_name))
                
    # TODO - handle if opponent is none, can set later by hitting /game/challenge/rival_id
    # TODO - send notification if rival_id is set
    
    @endpoints.method(request_message=GAME_LOOKUP_REQUEST,
                      response_message=StringMessage,
                      path='game/{game_id}',
                      name='read_game',
                      http_method='GET' )
                      
    def read_game(self, request):
        """Get info about current game"""
        # TODO - return json obj
        
        game = Game.query(Game.game_id == request.game_id).get()
        # note that primary key for Game is `game.key`
        if game:
            return StringMessage(message='Game with ID {} '.format(game.game_id))
        
        else:
            raise endpoints.BadRequestException('specified game_id not found')
                
# --- RUN ---
api = endpoints.api_server([AceofBlades])