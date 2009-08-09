#!/usr/bin/python
import twitter2
import re
from urllib2 import URLError, HTTPError

class OnDeafTweersReport(object):
	"""OnDeafTweers
	Class for comparing twitter followers and following
	to see who you're not following who you have had conversations
	with or have just @-replied you.
	"""
	"Constant for anything about the max freshhold"
	ABOVE_MAX = "20+"
	def __init__(self, api=None, searchApi=None, user=None, username=None, user_id=None):
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
		if username:
			self.user = self.api.GetUser(username)
		elif user_id:
			self.user = self.api.GetUser(user_id)
		else:
			self.user = user
		friendsIds = self.api.GetFriendsIds(user=user, username=username, user_id=user_id)
		followersIds = self.api.GetFollowersIds(user=user, username=username, user_id=user_id)
		# Get the difference between the 2, using sets
		# This gives us all followers that aren't also friends
		# Treat each as a User
		self.ids = set(followersIds).difference(set(friendsIds))
		self.at_username = "@%s" % self.user.GetScreenName()
		self.at_username_regex = re.compile(r"$%s" % self.at_username)

	def __iter__(self):
		return self.LookupFollowers()

	def LookupFollowers(self):
		user = self.user
		at_username = self.at_username
		at_username_regex = self.at_username_regex

		for id in ids:
			reportRow = {}
			try:
				follower = self.api.GetUser(id)
			except HTTPError:
				# Just skip any error in retrieving the user
				None
			else:
				# If the user has very few statuses, we may as well
				# try to query them instead
				if follower.GetStatusesCount() <= 5:
					try:
						statuses = follower.GetStatuses()
					except Exception:
						None
					else:
						for status in statuses:
							if at_username_regex.match(status):
								reportRow['to'] += 1
							elif at_username in status:
								reportRow['mentioned'] += 1
				else:
					# Do search here
					to_tweets = self.searchApi.Search(to_username=user.GetScreenName(), from_username=follower.GetScreenName(), per_page=20)
					if 'next_url' in to_tweets:
						reportRow['to'] = self.ABOVE_MAX
					else:
						reportRow['to'] = len(to_tweets['results'])
					reportRow['to_query'] = to_tweets['query']

					ref_tweets = self.searchApi.Search(referencing_username=user.GetScreenName(), from_username=follower.GetScreenName(), per_page=20)
					if 'next_url' in ref_tweets:
						reportRow['mentioned'] = self.ABOVE_MAX
					else:
						reportRow['mentioned'] = len(ref_tweets['results'])
					reportRow['mentioned_query'] = ref_tweets['query']

				reportRow["screen_name"] = follower.GetScreenName()
				yield reportRow

def main():
	# TODO: CLI
	#tbr = OnDeafTweersReport()
	print "ODT loaded"
	return

if __name__ == "__main__":
	main()
