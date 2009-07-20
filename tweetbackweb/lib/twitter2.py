import twitter
import simplejson

class Api(twitter.Api):
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

	def GetFollowersIds(self, userOrUserId, page=None):
		username = None
		if userOrUserId.__class__ == int:
			id = userOrUserId
		elif userOrUserId.__class__ == str:
			username = userOrUserId
		else:
			try:
				id = userOrUserId.id
			except AttributeError:
				raise Exception("First argument should be a User object or integer ID")
		if username:
			url = 'http://twitter.com/followers/ids/%s.json' % username
		else:
			url = 'http://twitter.com/followers/ids.json?user_id=%i' % id
		parameters = {}
		if page:
	  		parameters['page'] = page
		json = twitter.Api._FetchUrl(self, url, parameters=parameters)
		data = simplejson.loads(json)
		twitter.Api._CheckForTwitterError(self, data)
		return data

# TODO: figure out how to instatiate User objects from IDs
#
#	def GetFollowers(self, pageOrUserOrUserId=None):
#		if self._username:
#			twitter.Api.GetFollowers(self, pageOrUserOrUserId)
#		else:
#			ids = self.GetFollowers(pageOrUserOrUserId)
#			return [twitter.User(id) for id in ids]
