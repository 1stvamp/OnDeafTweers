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
		# Setup a nice constant for anything about the max freshhold
		self.ABOVE_MAX = "20+"

	def LookupFollowers(self, user=None, username=None, user_id=None):
		# TODO: lookup followers, lookup friends
		# search for @ replies by followers who aren't
		# friends, return dict() report
		if username:
			user = self.api.GetUser(username=username)
		elif user_id:
			user = self.api.GetUser(id=user_id)

		report = {}
		report["followers"] = {}
		at_username = "@%s" % user.GetScreenname()
		friendsIds = self.api.GetFriendsIds(user=user, username=username, user_id=user_id)
		followersIds = self.api.GetFollowersIds(user=user, username=username, user_id=user_id)
		# Get the difference between the 2, using sets
		# This gives us all followers that aren't also friends
		ids = set(followersIds).difference(set(friendsIds))
		# Treat each as a User
		followers = (self.api.GetUser(id=id) for id in ids)
		for follower in followers:
			if follower.GetScreenname() not in report["followers"]:
				# Make sure the sub-dict is instantiated
				report["followers"][follower.GetScreenname()] = {}
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
							report["followers"][follower.GetScreenname()]["mentioned"] += 1
			else:
				# Do search here
				to_tweets = self.searchApi.Search(to_username=user.GetScreenname(), from_username=follower.GetScreenname(), per_page=20)
				if 'next_url' in to_tweets:
					report["followers"][follower.GetScreenname()]["to"] = self.ABOVE_MAX
				else:
					report["followers"][follower.GetScreenname()]["to"] = len(to_weets['results'])
				report["followers"][follower.GetScreenname()]["to_query"] = to_tweets['query']

				ref_tweets = self.searchApi.Search(referencing_username=user.GetScreenname(), from_username=follower.GetScreenname(), per_page=20)
				if 'next_url' in ref_tweets:
					report["followers"][follower.GetScreenname()]["mentioned"] = self.ABOVE_MAX
				else:
					report["followers"][follower.GetScreenname()]["mentioned"] = len(ref_weets['results'])
				report["followers"][follower.GetScreenname()]["mentioned_query"] = ref_tweets['query']
		return None

def main():
	# TODO: CLI
	tb = OnDeafTweers()
	print "ODT loaded"
	return

if __name__ == "__main__":
	main()
