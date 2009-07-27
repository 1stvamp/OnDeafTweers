#!/usr/bin/python
import twitter2

class OnDeafTweers(object):
	"""OnDeafTweers
	Class for comparing twitter followers and following
	to see who you're not following who you have had conversations
	with or have just @-replied you.
	"""
	def __init__(self, api=None, searchApi=None):
		"Instantiate a OnDeafTweers object"
		if not api:
			# Twitter API wrapper not instantiated, so grab a new one
			self.api = twitter2.Api()
		else:
			self.api = api
		if not searchApi:
			self.searchApi = twitter2.SearchApi()
		else:
			self.searchApi = searchApi

	def LookupFollowers(self, user=None, username=None, user_id=None):
		# TODO: lookup followers, lookup friends
		# search for @ replies by followers who aren't
		# friends, return dict() report
		if username:
			user = self.api.GetUser(username=username)
		elif user_id:
			user = self.api.GetUser(id=user_id)

		friendsIds = self.api.GetFriendsIds(user=user, username=username, user_id=user_id)
		followersIds = self.api.GetFollowersIds(user=user, username=username, user_id=user_id)
		# Get the difference between the 2, using sets
		# This gives us all followers that aren't also friends
		ids = set(followersIds).difference(set(friendsIds))
		# Treat each as a User
		users = (self.api.GetUser(id=id) for id in ids)
		for user in users:
			# Do search here
			query = "@%s" % user.name
		return None

def main():
	tb = OnDeafTweers()
	print "ODT loaded"
	return

if __name__ == "__main__":
	main()
