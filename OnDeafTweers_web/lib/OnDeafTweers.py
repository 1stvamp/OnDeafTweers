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

		report = {}
		at_username = "@%s" % user.GetScreenname()
		friendsIds = self.api.GetFriendsIds(user=user, username=username, user_id=user_id)
		followersIds = self.api.GetFollowersIds(user=user, username=username, user_id=user_id)
		# Get the difference between the 2, using sets
		# This gives us all followers that aren't also friends
		ids = set(followersIds).difference(set(friendsIds))
		# Treat each as a User
		users = (self.api.GetUser(id=id) for id in ids)
		for user in users:
			# If the user has very few statuses, we may as well
			# try to query them instead
			if user.GetStatusesCount() <= 5:
				try:
					statuses = user.GetStatuses()
				except Exception:
					None
				else:
					for status in statuses:
						if at_username in status:
							if not report["followers"][user.GetScreenname()]:
								# Make sure the sub-dict is instantiated
								report["followers"][user.GetScreenname()] = {}
							report["followers"][user.GetScreenname()]["mentioned"] += 1
							if "RT" in status:
								report["followers"][user.GetScreenname]["retweets"] += 1
			else:
				# Do search here
				to_tweets = self.searchApi.Search()
				ref_tweets = self.searchApi.Search()
		return None

def main():
	# TODO: CLI
	tb = OnDeafTweers()
	print "ODT loaded"
	return

if __name__ == "__main__":
	main()
