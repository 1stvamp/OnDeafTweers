<%
from pylons.templating import render_mako as render
st_output = render(sub_template)
%>
${st_output}
