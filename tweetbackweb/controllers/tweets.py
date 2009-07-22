import logging
import sys

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from tweetbackweb.lib.base import BaseController, render

import twitter2
from tweetback import Tweetback
from urllib2 import URLError, HTTPError

log = logging.getLogger(__name__)

class TweetsController(BaseController):
	def __before__(self):
		# Make sure we have a Tweetback instance
		self.tb = Tweetback()
		# And a twitter2.Api instance for users
		self.tw = twitter2.Api()

	def user(self):
		if session['twitter_user']:
			c.twitter_user = session['twitter_user']
			c.report = self.tb.LookupFollowers(session['twitter_user'])
			return render('/tweets/report_user.mako')
		else:
			return render('/tweets/new_user.mako')

	def new_user(self, id):
		try:
			session['twitter_user'] = self.tw.GetUser(id)
		except HTTPError exception:
			c.id = id
			c.exception = exception
			return render('/tweets/new_user_error.mako')
		session.save()
		redirect_to('/tweets/user')

