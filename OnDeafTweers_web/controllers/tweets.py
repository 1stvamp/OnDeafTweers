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
		if "twitter_users" not in session:
			session["twitter_users"] = {}

		if id not in session["twitter_users"]:
			try:
				user = self.tw.GetUser(id)
			except HTTPError, e:
				c.id = id
				c.exception = e
				return render('/tweets/new_user_error.mako')
			else:
				session["twitter_users"][id] = user
		else:
			user = session["twitter_users"][id]

		if "twitter_user_reports" not in session:
			session["twitter_user_reports"] = {}
		
		if id not in session["twitter_user_reports"]:
			report = self.odt.LookupFollowers(user=user)
			session["twitter_user_reports"][id] = report
		else:
			report = session["twitter_user_reports"][id]

		session.save()

		c.report = report
		c.twitter_user = user
		return render('/tweets/user_report.mako')

