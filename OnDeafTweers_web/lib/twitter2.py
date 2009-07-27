#!/usr/bin/env python

"""A class that inherits from python-twitter, but provides extended
API methods and oAuth authentication.

Requires:
	python-twitter
	simplejson
	oauth

oAuth code adapted from oauth-python-twitter v0.2 by Hameedullah Khan <hameed@hameedkhan.net>

Copyright 2009 Wesley Mason

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU  Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__author__ = "Wesley Aaron Mason <wes@1stvamp.org>"
__version__ = "1.0"

import twitter, simplejson, oauth
from oauth import oauth
from urllib2 import URLError, HTTPError


# Taken from oauth implementation at: http://github.com/harperreed/twitteroauth-python/tree/master
REQUEST_TOKEN_URL = 'https://twitter.com/oauth/request_token'
ACCESS_TOKEN_URL = 'https://twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'http://twitter.com/oauth/authorize'
SIGNIN_URL = 'http://twitter.com/oauth/authenticate'

class Api(twitter.Api):
	def __init__(self, username=None, password=None, input_encoding=None, request_headers=None,
			consumer_key=None, consumer_secret=None, access_token=None):
		"""Instantiate a Twitter2 extended Api object
		This inherits from Twitter.Api but provides extra Twitter API
		methods (GetFollowersIds) and functionality (oAuth authentication).
		Args:
			username: The username of the twitter account.  [optional]
			password: The password for the twitter account. [optional]
			input_encoding: The encoding used to encode input strings. [optional]
			request_header: A dictionary of additional HTTP request headers. [optional]
		"""
		if access_token:
			twitter.Api.__init__(self, access_token.key, access_token.secret, input_encoding, request_headers)
		else:
			twitter.Api.__init__(self, username, password, input_encoding, request_headers)
		if consumer_key or consumer_secret:
			self._Consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
		else:
			self._Consumer = None
		self._signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
		self._access_token = access_token

	def GetFollowersIds(self, user_id=None, username=None, user=None, page=None):
		"""Retrieve a list() of user IDs for a User's followers.
		Like GetFollowers() but only returns IDs, not full User
		objects.
		If user, username or user ID has been ommited, then the authenticated
		(if present) user is used.
		Args:
		"""
		if user_id:
			id = user_id
		elif username:
			None
		elif user:
			id = user.id
		elif self._username:
			 id = self._username.id
		else:
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
		If username or user ID has been ommited, then the authenticated
		(if present) user is used.
		Args:
			page: If calling by username or ID, you can optionally provide
				a page of followers to display. [optional]
			username:
			user_id:
		"""
		if username or user_id:
			ids = self.GetFollowersIds(username=username, user_id=user_id, page=page)
			users = []
			for id in ids:
				try:
					users.append(self.GetUser(id))
				except (HTTPError, URLError):
					None
			return users
		elif self._username:
			return twitter.Api.GetFollowers(self, page)
		else:
			raise Exception("GetFollowers() requires username or user_id or an authenticated User")

	def GetFriendsIds(self, user=None, username=None, user_id=None, page=None):
		"""Retrieve a list() of user IDs for a User's friends.
		Like GetFriends() but only returns IDs, not full User
		objects.
		If user, username or user ID has been ommited, then the authenticated
		(if present) user is used.
		Args:
			user:
			username:
			user_id:
			page:
		"""
		if user_id:
			id = user_id
		elif username:
			None
		elif user:
			id = user.id
		elif self._username:
			 id = self._username.id
		else:
			raise Exception("No Api.User, user ID or username provided")

		if username:
			url = 'http://twitter.com/friends/ids/%s.json' % username
		else:
			url = 'http://twitter.com/friends/ids.json?user_id=%i' % id
		parameters = {}
		if page:
			parameters['page'] = page
		json = self._FetchUrl(url, parameters=parameters)
		data = simplejson.loads(json)
		self._CheckForTwitterError(data)
		return data

	# oAuth methods
	def _FetchUrl(self, url, post_data=None, parameters=None, no_cache=None):
		"""Fetch a URL, optionally caching for a specified time.
		Overrides twitter.Api._FetchUrl() to switch between
		non-oAuth authenticated requests and oAuth authenticated
		requests.
		
		Args:
		url: The URL to retrieve
		post_data: 
			A dict of (str, unicode) key/value pairs.  If set, POST will be used.
		parameters:
			A dict whose key/value pairs should encoded and added 
			to the query string. [OPTIONAL]
		no_cache: If true, overrides the cache on the current request
	
		Returns:
		A string containing the body of the response.
		"""
		if self._Consumer:
			return self._OAuthFetchUrl(self, url, post_data=post_data, parameters=parameters, no_cache=no_cache)
		else:
			return twitter.Api._FetchUrl(self, url, post_data=post_data, parameters=parameters, no_cache=no_cache)

	def _OAuthFetchUrl(self, url, post_data=None, parameters=None, no_cache=None):
		"""Fetch a URL, optionally caching for a specified time, using
		oAuth for request authentication.
			
		Args:
		url: The URL to retrieve
		post_data: 
			A dict of (str, unicode) key/value pairs.  If set, POST will be used.
		parameters:
			A dict whose key/value pairs should encoded and added 
			to the query string. [OPTIONAL]
		no_cache: If true, overrides the cache on the current request
	
		Returns:
		A string containing the body of the response.
		"""
		# Build the extra parameters dict
		extra_params = {}
		if self._default_params:
			extra_params.update(self._default_params)
		if parameters:
			extra_params.update(parameters)
	
		# Add key/value parameters to the query string of the url
		#url = self._BuildUrl(url, extra_params=extra_params)
	
		if post_data:
			http_method = "POST"
			extra_params.update(post_data)
		else:
			http_method = "GET"
		
		req = self._MakeOAuthRequest(url, parameters=extra_params, http_method=http_method)
		self._signRequest(req, self._signature_method)
		
		# Get a url opener that can handle Oauth basic auth
		opener = self._GetOpener()
		
		#encoded_post_data = self._EncodePostData(post_data)

		if post_data:
			encoded_post_data = req.to_postdata()
			url = req.get_normalized_http_url()
		else:
			url = req.to_url()
			encoded_post_data = ""
			
		no_cache = True
		# Open and return the URL immediately if we're not going to cache
		# OR we are posting data
		if encoded_post_data or no_cache:
			if encoded_post_data:
				url_data = opener.open(url, encoded_post_data).read()
			else:
				url_data = opener.open(url).read()
				opener.close()
		else:
			# Unique keys are a combination of the url and the username
			if self._username:
				key = self._username + ':' + url
			else:
				key = url
	
		# See if it has been cached before
		last_cached = self._cache.GetCachedTime(key)
	
		# If the cached version is outdated then fetch another and store it
		if not last_cached or time.time() >= last_cached + self._cache_timeout:
			url_data = opener.open(url).read()
			opener.close()
			self._cache.Set(key, url_data)
		else:
			url_data = self._cache.Get(key)
	
		# Always return the latest version
		return url_data
	
	def _MakeOAuthRequest(self, url, token=None, parameters=None, http_method="GET"):
		"""Make a OAuth request from url and parameters
		
		Args:
			url: The Url to use for creating OAuth Request
			parameters: The URL parameters
			http_method: The HTTP method to use
		Returns:
		A OAauthRequest object
		"""
		if not token:
			token = self._access_token
		request = oauth.OAuthRequest.from_consumer_and_token(self._Consumer, token=token, http_url=url, parameters=parameters, http_method=http_method)
		return request

	def _signRequest(self, req, signature_method=oauth.OAuthSignatureMethod_HMAC_SHA1()):
		"""Sign a request
		
		Reminder: Created this function so incase
		if I need to add anything to request before signing
		
		Args:
			req: The oAuth request created via _MakeOAuthRequest
			signate_method: The oAuth signature method to use
		"""
		req.sign_request(signature_method, self._Consumer, self._access_token)

	def GetAuthorizationUrl(self, token, url=AUTHORIZATION_URL):
		"""Create a signed authorization URL
		
		Returns:
			A signed OAuthRequest authorization URL 
		"""
		req = self._MakeOAuthRequest(url, token=token)
		self._signRequest(req)
		return req.to_url()

	def GetSignInUrl(self, token, url=SIGNIN_URL):
		"""Create a signed Sign-in URL
		
		Returns:
			A signed OAuthRequest Sign-in URL 
		"""
		
		signin_url = self.GetAuthorizationUrl(token, url)
		return signin_url
	
	def GetAccessToken(self, url=ACCESS_TOKEN_URL):
		token = self._FetchUrl(url, no_cache=True)
		return oauth.OAuthToken.from_string(token) 

	def GetRequestToken(self, url=REQUEST_TOKEN_URL):
		"""Get a Request Token from Twitter
		
		Returns:
			A OAuthToken object containing a request token
		"""
		resp = self._FetchUrl(url, no_cache=True)
		token = oauth.OAuthToken.from_string(resp)
		return token
	
	def GetUserInfo(self, url='https://twitter.com/account/verify_credentials.json'):
		"""Get user information from twitter
		
		Returns:
			Returns the twitter.User object
		"""
		json = self._FetchUrl(url)
		data = simplejson.loads(json)
		self._CheckForTwitterError(data)
		return User.NewFromJsonDict(data)


class SearchApi(Api):
	def __init__(self):
		Api(self)

	def Search(self, query=None, phrase=None, until_date=None, since_date=None, language=None,
			page=None, number_of_pages=15, since_id=None, to_user=None, from_user=None,
			referencing_user=None, tag=None, and_query=None, or_query=None, not_query=None,
			within=None, near=None, location_units="mi"):
		"""Search Twitter for tweets matching given terms
		Args:
		"""
		# Make sure that at least one optional arg was passed
		args = [element for element in locals() if element]
		if not args:
			raise Exception("Search() requires at least one arg")
		url = "http://search.twitter.com/search.json"
		parameters = {}
		if page:
			parameters['page'] = page
		if query:
			parameters['q'] = query
		if phrase:
			parameters['phrase'] = phrase
		if until_date:
			parameters['until'] = until_date
		if since_date:
			parameters['since'] = since_date
		if language:
			parameters['lang'] = language
		if number_of_pages:
			parameters['rpp'] = number_of_pages
		if since_id:
			parameters['since_id'] = since_id
		if to_user:
			parameters['to'] = to_user
		if from_user:
			parameters['from'] = from_user
		if referencing_user:
			parameters['ref'] = referencing_user
		if tag:
			parameters['tag'] = tag
		if and_query:
			parameters['ands'] = and_query
		if or_query:
			parameters['ors'] = or_query

		json = self._FetchUrl(url, parameters=parameters)
		data = simplejson.loads(json)
		self._CheckForTwitterError(data)
		return []

class User(twitter.User):
	def __init__(self, id=None, name=None, screen_name=None, location=None, description=None, profile_image_url=None, profile_background_tile=None, profile_background_image_url=None, profile_sidebar_fill_color=None, profile_background_color=None, profile_link_color=None, profile_text_color=None, protected=None, utc_offset=None, time_zone=None, followers_count=None, friends_count=None, statuses_count=None, favourites_count=None, url=None, status=None):
		"""twitter2 wrapper around twitter.User, allowing you to
		call User methods and the User class from a single module
		(twitter2) rather than having to import python-twitter as
		well.
		"""
		twitter.User.__init__(self, id=id, name=name, screen_name=screen_name, location=location, description=description, profile_image_url=profile_image_url, profile_background_tile=profile_background_tile, profile_background_image_url=profile_background_image_url, profile_sidebar_fill_color=profile_sidebar_fill_color, profile_background_color=profile_background_color, profile_link_color=profile_link_color, profile_text_color=profile_text_color, protected=protected, utc_offset=utc_offset, time_zone=time_zone, followers_count=followers_count, friends_count=friends_count, statuses_count=statuses_count, favourites_count=favourites_count, url=url, status=status);
