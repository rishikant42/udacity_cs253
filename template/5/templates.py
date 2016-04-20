import os
import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates') #pwd/templates
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

hidden_html = """
<input type="hidden" name="food" value="%s">
"""

item_html = "<li>%s</li>"

shopping_list_html = """
<br><br>
<h2>Shopping List</h2>
<ul>
%s
</ul>
"""

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):  ##**parmas, use if we pass extra prmtr
											   ## i.e value in htlm file format {{variable}}
		t = jinja_env.get_template(template)   ## load the specify template, html file
		return t.render(params)                ## render html file with passing prmtrs(put value of prmtr)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))

class MainPage(Handler):
	def get(self):
		self.render("shopping_list.html", name="udacity")

##		output = form_html
##		output_hidden = ""
##		
##		items = self.request.get_all("food")
##		if items:
##			output_items = ""
##			for item in items:
##				output_hidden += hidden_html % item
##				output_items += item_html % item
##
##			output_shopping = shopping_list_html % output_items
##			output += output_shopping
##
##		output = output % output_hidden
##
##		self.write(output)

app = webapp2.WSGIApplication([('/', MainPage),], debug=True)
