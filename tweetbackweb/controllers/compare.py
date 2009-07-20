import logging
import sys

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from tweetbackweb.lib.base import BaseController, render

from tweetback import tweetback

log = logging.getLogger(__name__)

class CompareController(BaseController):

    def index(self):
        # Return a rendered template
        return render('/compare.mako')
