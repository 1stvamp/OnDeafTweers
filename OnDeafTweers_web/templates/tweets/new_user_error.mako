% if c.exception.errno == 404
	User not found
% elif c.exception.errno == 501
	User not public
