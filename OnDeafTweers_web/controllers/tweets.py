import logging
import sys

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to

from OnDeafTweers_web.lib.base import BaseController, render

from pylons.decorators import jsonify
import simplejson

import twitter2
from OnDeafTweersReport import OnDeafTweersReport
from urllib2 import URLError, HTTPError

log = logging.getLogger(__name__)

class TweetsController(BaseController):
	def __before__(self):
		# twitter2.Api instance for users
		self.tw = twitter2.Api()
		# Only use python-memcache if it's available
		try:
			import memcache
		except ImportError:
			self.mc = None
		else:
			# TODO: init mc server list from config and pass it into Client()
			self.mc = memcache.Client(['127.0.0.1:11211'], debug=0)

	@jsonify
	def generate_report(self, id):
		try:
			report = self.get_report(self.get_user(id))
		except HTTPError as e:
			c.id = id
			c.exception = e
			return render('/tweets/new_user_error.mako')
		return report

	def home(self):
		return render('/home.mako');

	def get_user(self, id):
		user = None
		if self.mc:
			# Use memcache
			user = self.mc.get("twitter_user_%s" % id)
		else:
			# Use sessions
			if "twitter_users" not in session:
				session["twitter_users"] = {}

			if id in session["twitter_users"]:
				user = session["twitter_users"][id]
			else:
				user = None

		if not user:
			user = self.tw.GetUser(id)
			self.set_user(id, user)
		return user
	
	def set_user(self, id, user):
		if self.mc:
			# Use memcache
			self.mc.set("twitter_user_%s" % id, user)
		else:
			# Use sessions
			if "twitter_users" not in session:
				session["twitter_users"] = {}

			session["twitter_users"][id] = user
			session.save()

	def get_report(self, user):
		report = None
		if self.mc:
			# Use memcache
			report = self.mc.get("twitter_user_report_for_%s" % id)
		else:
			# Use sessions
			if "twitter_user_reports" not in session:
				session["twitter_user_reports"] = {}
			
			if id in session["twitter_user_reports"]:
				report = session["twitter_user_reports"][id]
			else:
				report = None
		
		if not report:
			# Set the total number of followers in the session
			# so we can show the current status via Ajax
			session["follower_count"] = user.GetFollowersCount()
			session.save()
			report_generator = (row for row in OnDeafTweersReport(api=self.tw, user=user))
			report = []
			session["follower_current_num"] = 0;
			for row in report_generator:
				# Set the current follower number, to display
				# the current status via Ajax
				session["follower_current_num"] += 1
				session.save()
				report.append(row)

			self.set_report(user.GetID(), report)
		return report

	@jsonify
	def get_follower_count(self):
		return dict(count=session["follower_count"])

	@jsonify
	def get_follower_current_num(self):
		return dict(num=session["follower_current_num"])

	def set_report(self, id, report):
		if self.mc:
			# Use memcache
			self.mc.set("twitter_user_report_for_%s" % id, report)
		else:
			# Use sessions
			if "twitter_user_reports" not in session:
				session["twitter_user_reports"] = {}

			session["twitter_user_reports"][id] = report
			session.save()
