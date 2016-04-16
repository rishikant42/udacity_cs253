import webapp2
import string
import jinja2
import os

upper = string.letters[:26]
upper_c = upper[13:] + upper[:13]
lower = string.letters[26:]
lower_c = lower[13:] + lower[:13]
dic = {}
for i in range(26):
    dic[upper[i]] = upper_c[i]
for i in range(26):
    dic[lower[i]] = lower_c[i]

def encypher(text):
    cypher = ""
    for c in text:
        if c in string.letters:
            cypher += dic[c]
        else: cypher += c
    return cypher


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

class ROT13(BaseHandler):
    def get(self):
        self.render('main.html')

    def post(self):
        rot13 = self.request.get("text")
        if rot13:
            rot13 = encypher(rot13)
        self.render('main.html', text=rot13)

application = webapp2.WSGIApplication([('/', ROT13)], debug=True)
