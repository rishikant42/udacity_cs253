import webapp2
import jinja2
import os
import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                               autoescape=True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{4,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **params):
        self.response.out.write(render_str(template, **params))

class Signup(BaseHandler):
    def get(self):
        self.render('signup.html')

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username=username, email=email)

        if not username or not USER_RE.match(username):
            have_error = True
            params['error_username'] = "that's not a valid username."
        if not password or not PASS_RE.match(password):
            have_error = True
            params['error_password'] = "that's not a valid password."
        if password != verify:
            have_error = True
            params['error_verify'] = "passwords didn't match."
        if email and not EMAIL_RE.match(email):
            have_error = True
            params['error_email'] = "that's not a valid email address."
        if have_error:
            self.render('signup.html', **params)
        else:
            self.redirect('/welcome?usernames='+username)

class Welcome(BaseHandler):
    def get(self):
        username = self.request.get('usernames')
        if username and USER_RE.match(username):
            self.render('welcome.html', username=username)
        else:
            self.redirect('/')


application = webapp2.WSGIApplication([('/', Signup),
                                       ('/welcome', Welcome)],
                                      debug=True)
