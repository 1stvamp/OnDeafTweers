from tweetbackweb.tests import *

class TestTweetsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='compare', action='index'))
        # Test response...
