#!/usr/bin/python
import twitter2
from urllib2 import URLError, HTTPError

class OnDeafTweers(object):
	"""OnDeafTweers
	Class for comparing twitter followers and following
	to see who you're not following who you have had conversations
	with or have just @-replied you.
	"""
	"Constant for anything about the max freshhold"
	ABOVE_MAX = "20+"
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
			user = self.api.GetUser(username)
		elif user_id:
			user = self.api.GetUser(user_id)

		report = {}
		report["followers"] = {}
		at_username = "@%s" % user.GetScreenName()
		friendsIds = self.api.GetFriendsIds(user=user, username=username, user_id=user_id)
		followersIds = self.api.GetFollowersIds(user=user, username=username, user_id=user_id)
		# Get the difference between the 2, using sets
		# This gives us all followers that aren't also friends
		ids = set(followersIds).difference(set(friendsIds))
		# Treat each as a User
		for id in ids:
			try:
				follower = self.api.GetUser(id)
			except HTTPError:
				# Just skip any error in retrieving the user
				None
			else:
				if follower.GetScreenName() not in report["followers"]:
					# Make sure the sub-dict is instantiated
					report["followers"][follower.GetScreenName()] = {}
				# If the user has very few statuses, we may as well
				# try to query them instead
				if follower.GetStatusesCount() <= 5:
					try:
						statuses = follower.GetStatuses()
					except Exception:
						None
					else:
						for status in statuses:
							# TODO: add to_tweets equiv here
							if at_username in status:
								report["followers"][follower.GetScreenName()]["mentioned"] += 1
				else:
					# Do search here
					to_tweets = self.searchApi.Search(to_username=user.GetScreenName(), from_username=follower.GetScreenName(), per_page=20)
					if 'next_url' in to_tweets:
						report["followers"][follower.GetScreenName()]["to"] = self.ABOVE_MAX
					else:
						report["followers"][follower.GetScreenName()]["to"] = len(to_tweets['results'])
					report["followers"][follower.GetScreenName()]["to_query"] = to_tweets['query']

					ref_tweets = self.searchApi.Search(referencing_username=user.GetScreenName(), from_username=follower.GetScreenName(), per_page=20)
					if 'next_url' in ref_tweets:
						report["followers"][follower.GetScreenName()]["mentioned"] = self.ABOVE_MAX
					else:
						report["followers"][follower.GetScreenName()]["mentioned"] = len(ref_tweets['results'])
					report["followers"][follower.GetScreenName()]["mentioned_query"] = ref_tweets['query']
		return report

def main():
	# TODO: CLI
	tb = OnDeafTweers()
	print "ODT loaded"
	return

if __name__ == "__main__":
	main()
