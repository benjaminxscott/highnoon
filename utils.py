"""utils.py - File for collecting general utility functions."""

import logging
from google.appengine.ext import ndb
import endpoints
import uuid
import base64


def uniq_id():
    # generate a urlsafe and copy/pastable uid
    # ref http://stackoverflow.com/a/10984286
    r_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
    r_uuid = r_uuid.translate(None, '_=-')
    return r_uuid
