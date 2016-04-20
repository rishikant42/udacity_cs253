import os
import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates') #pwd/templates
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

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
		items = self.request.get_all("food")
		self.render("shopping_list.html", items = items)

app = webapp2.WSGIApplication([('/', MainPage),], debug=True)
