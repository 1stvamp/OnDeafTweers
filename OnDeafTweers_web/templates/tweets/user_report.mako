<%inherit file="base.mako"/>
report:<br/>
% for key,value in c.report.iteritems():
	${key} = ${value}
% endfor
