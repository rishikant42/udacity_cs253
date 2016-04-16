import jinja2
import webapp2
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

#def render_str(template, **params):
#    t = jinja_env.get_template(template)
#    return t.render(params)

class MainPage(webapp2.RequestHandler):
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)
    def render(self, template, **kw):
        self.response.out.write(self.render_str(template, **kw))

class new(MainPage):
    def get(self):
        self.render("main.html",name="rishi")

app = webapp2.WSGIApplication([
        ('/', new)], debug=True)
