import logging
import sys

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from OnDeafTweers_web.lib.base import BaseController, render

import twitter2
from OnDeafTweers import OnDeafTweers
from urllib2 import URLError, HTTPError

log = logging.getLogger(__name__)

class TweetsController(BaseController):
	def __before__(self):
		# twitter2.Api instance for users
		self.tw = twitter2.Api()
		# Make sure we have a Tweetback instance
		# also pass in the API instance for reuse
		self.odt = OnDeafTweers(self.tw)

	def user(self, id):
		try:
			session['twitter_user'] = self.tw.GetUser(id)
		except HTTPError as exception:
			c.id = id
			c.exception = exception
			return render('/tweets/new_user_error.mako')
		else:
			session.save()

		c.twitter_user = session['twitter_user']
		c.report = self.odt.LookupFollowers(user=session['twitter_user'])
		return render('/tweets/user_report.mako')

