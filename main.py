import webapp2
import os
import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class User(ndb.Model):
    name = ndb.StringProperty()
    blurb = ndb.StringProperty()

class Artist(ndb.Model):
    name = ndb.StringProperty()
    bio = ndb.StringProperty()
    images = ndb.StringProperty()

class Preference(ndb.Model):
    user_key = ndb.KeyProperty(kind=Post)
    artist_key = ndb.KeyProperty(kind=Post)
    like = ndb.IntegerProperty()

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')
        template = jinja_environment.get_template('templates/log_in_page.html')
        self.response.write(template.render())

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')
        template = jinja_environment.get_template('templates/home.html')
        self.response.write(template.render())

class ArtistHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/artist_page.html')
        self.response.write(template.render())

class ProfileHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/profile.html')
        self.response.write(template.render())


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('login', LoginHandler),
    ('artist', ArtistHandler),
    ('profile',ProfileHandler)
], debug=True)
