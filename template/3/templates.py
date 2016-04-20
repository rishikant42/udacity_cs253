import os
import webapp2

form_html = """
<form>
<h2>Add a Food</h2>
<input type="text" name="food">
<button>Add</button>
</form>
"""

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.out.write(form_html)

app = webapp2.WSGIApplication([('/', MainPage),], debug=True)
