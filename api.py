# -*- coding: utf-8 -*-`

import logging
import endpoints
from protorpc import remote, messages
from google.appengine.api import memcache
from google.appengine.api import taskqueue

from models import User, UserMessage
from models import StringMessage
from utils import get_by_urlsafe, generate_player_id

# DBG import bleach
# DBG from profanity import contains_profanity

USER_REQUEST = endpoints.ResourceContainer(UserMessage)

@endpoints.api(name='aceofblades', version='v1')
class AceofBlades(remote.Service):
    """Game API"""
    @endpoints.method(request_message=USER_REQUEST,
                      response_message=StringMessage,
                      path='user',
                      name='create_user',
                      http_method='POST' )
    def create_user(self, request):
        """Create a User. Optionally set a (non)unique username"""
        
        '''
        if contains_profanity(request.user_name)
            raise endpoints.BadRequestException(
                    'player_name was not valid - perhaps it contained profanity')
        '''
        
        player_name = None
        if request.desired_name is not None:
            # DBG player_name = str(bleach.clean(request.desired_name))
            player_name = request.desired_name
            
        player_id = generate_player_id()
        
        user = User(player_id = player_id, player_name=player_name)
        user.put()
        
        # TODO return id and name as json instead
        return StringMessage(message='Player {} with ID {} has stepped through the door'.format(
                player_name, player_id))


api = endpoints.api_server([AceofBlades])