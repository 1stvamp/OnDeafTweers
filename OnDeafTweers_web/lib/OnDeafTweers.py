#!/usr/bin/python
import twitter2

class OnDeafTweers(object):
	"""OnDeafTweers
	Class for comparing twitter followers and following
	to see who you're not following who you have had conversations
	with or have just @-replied you.
	"""
	def __init__(self, user=None):
		"Instantiate a OnDeafTweers object"
		self.user = user

	def LookupFollowers(self, user=None, username=None, user_id=None):
		# TODO: lookup followers, lookup friends
		# search for @ replies by followers who aren't
		# friends, return dict() report
		return None

def main():
	tb = OnDeafTweers()
	print "tweetback loaded"
	return

if __name__ == "__main__":
	main()
