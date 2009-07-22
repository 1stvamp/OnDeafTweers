import logging
import sys

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from tweetbackweb.lib.base import BaseController, render

import twitter2
from tweetback import Tweetback

log = logging.getLogger(__name__)

class TweetsController(BaseController):
	def __before__(self):
		# Make sure we have a Tweetback instance
		self.tb = Tweetback()
		# And a twitter2.Api instance for users
		self.tw = twitter2.Api()

	def user(self):
		if session['twitter_user']:
			report = self.tb.LookupFollowers(session['twitter_user'])
			return render('/tweets/report_user.mako')
		else:
			return render('/tweets/new_user.mako')

	def new_user(self, id):
		session['twitter_user'] = self.tw.GetUser(id)
		session.save()
		redirect_to('/tweets/user')

