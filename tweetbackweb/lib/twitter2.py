import twitter
import simplejson
from urllib2 import URLError, HTTPError
import oath

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

	# TODO: Change this to use named args instead of a multi-type single arg
	def GetFollowersIds(self, userOrUsernameOrUserId, page=None):
		"Get a list() of following user IDs"
		username = None
		if userOrUsernameOrUserId.__class__ == int:
			id = userOrUsernameOrUserId
		elif userOrUsernameOrUserId.__class__ == str:
			username = userOrUsernameOrUserId
		else:
			try:
				id = userOrUsernameOrUserId.id
			except AttributeError:
				raise Exception("First argument should be a User object or integer ID")
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

	# TODO: Change this to use named args instead of a multi-type single arg
	def GetFollowers(self, pageOrUsernameOrUserId=None, page=None):
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
			ids = self.GetFollowersIds(pageOrUsernameOrUserId, page)
			users = []
			for id in ids:
				try:
					users.append(self.GetUser(id))
				except (HTTPError, URLError):
					"skip"
			return users
