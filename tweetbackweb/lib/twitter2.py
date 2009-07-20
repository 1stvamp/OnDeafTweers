import twitter
import simplejson
from urllib2 import URLError, HTTPError

class Api(twitter.Api):
	# TODO: Add oAuth in
	def __init__(self, username=None, password=None, input_encoding=None, request_headers=None):
		"""Instantiate a Twitter2 extended Api object
		This inherits from Twitter.Api but provides extra Twitter API
		methods (GetFollowersIds) and functionality (oAuth authentication).
		Args:
			username: The username of the twitter account.  [optional]
			password: The password for the twitter account. [optional]
			input_encoding: The encoding used to encode input strings. [optional]
			request_header: A dictionary of additional HTTP request headers. [optional]
		"""
		twitter.Api.__init__(self, username, password, input_encoding, request_headers)
		self.oauth_handler = oath_handler

	def GetFollowersIds(self, user_id=None, username=None, user=None, page=None):
		"Get a list() of following user IDs"
		if user_id:
			id = user_id
		elif user:
			id = user.id
		else not username:
			raise Exception("No Api.User, user ID or username provided")
		if username:
			url = 'http://twitter.com/followers/ids/%s.json' % username
		else:
			url = 'http://twitter.com/followers/ids.json?user_id=%i' % id
		parameters = {}
		if page:
	  		parameters['page'] = page
		json = self._FetchUrl(url, parameters=parameters)
		data = simplejson.loads(json)
		self._CheckForTwitterError(data)
		return data

	def GetFollowers(self, page=None, username=None, user_id=None):
		"""Extended version of twitter.Api.GetFollowers
		Doesn't require an authenticated User instance, as it will
		alternatively use GetFollowersIds() to retrieve a list of
		user IDs and then instantiate a list() of User objects
		by ID.
		If a User has been authenticated, the parent method will
		be called instead.
		Args:
			pageOrUserOrUserId: If a User is authenticated you can pass in
				a page number, otherwise you need to pass in a username
				or an ID.
			page: If calling by username or ID, you can optionally provide
				a page of followers to display. [optional]
		"""
		if self._username:
			twitter.Api.GetFollowers(self, pageOrUsernameOrUserId)
		else:
			ids = self.GetFollowersIds(username=username, user_id=user_id, page=page)
			users = []
			for id in ids:
				try:
					users.append(self.GetUser(id))
				except (HTTPError, URLError):
					"skip"
			return users
