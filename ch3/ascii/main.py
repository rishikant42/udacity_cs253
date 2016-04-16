import os
import webapp2
import jinja2
import sys
import re
from xml.dom import minidom
from string import letters
import urllib2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

GMAPS_URL = "https://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false&"
def gmaps_img(points):
    markers = '&'.join('markers=%s,%s' %(p.lat, p.lon)
                        for p in points)
    return GMAPS_URL + markers

IP_URL = "http://api.hostip.info/?ip="
def get_coords(ip):
    ip = "4.2.2.2"
    ip = "23.24.209.141"
    url = IP_URL + ip
    content = None
    try:
        content = urllib2.urlopen(url).read()
    except:
        return
    if content:
        d = minidom.parseString(content)
        coords = d.getElementsByTagName("gml:coordinates")
        if coords and coords[0].childNodes[0].nodeValue:
            lon, lat = coords[0].childNodes[0].nodeValue.split(',')
            return db.GeoPt(lat, lon)

class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    coords = db.GeoPtProperty()
     

class MainPage(Handler):
    def render_front(self, title="", art="", error=""):
	arts = db.GqlQuery("SELECT * FROM Art "
			   "ORDER BY created DESC LIMIT 10")
	#arts = db.GqlQuery("SELECT * " "FROM Art " "WHERE ANCESTOR IS :1"
	#		   "ORDER BY created DESC " "LIMIT 10")
	arts = list(arts)
	points = filter(None, (a.coords for a in arts))

	img_url = None
	if points:
            img_url = gmaps_img(points)
	
	self.render("form.html", title=title, art=art, error=error, arts=arts, img_url = img_url)

    def get(self):
        self.write(self.request.remote_addr)
        self.write(repr(get_coords(self.request.remote_addr)))
	return self.render_front()

    def post(self):
	title = self.request.get("title")
	art = self.request.get("art")

	if title and art:
	   #self.write("thanks!")
	    a = Art(title = title, art = art)
	    coords = get_coords(self.request.remote_addr)
	    if coords:
                a.coords = coords
	    a.put()
	    self.redirect("/")	    
	else:
	    error = "we need both a title and some art work!"
	    self.render_front(title, art, error)


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)

