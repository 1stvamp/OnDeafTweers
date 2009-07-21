#!/usr/bin/python
import twitter2

class Tweetback(object):
	"""Tweetback
	Class for comparing twitter followers and following
	to see who you're not following who you have had conversations
	with or have just @-replied you.
	"""
	def __init__(self, user=None):
		"Instantiate a Tweetback object"
		self.user = user

	def LookupFollowers(self, user):
		# TODO: lookup followers, lookup friends
		# search for @ replies by followers who aren't
		# friends, return dict() report
		return None

def main():
	tb = Tweetback()
	print "tweetback loaded"
	return

if __name__ == "__main__":
	main()
