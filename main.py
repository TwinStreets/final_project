import webapp2
import os
import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

# This is the user profile
class User(ndb.Model):
    name = ndb.StringProperty()
    blurb = ndb.StringProperty()

# This is the artist profile
class Artist(ndb.Model):
    name = ndb.StringProperty()
    bio = ndb.StringProperty()
    images = ndb.StringProperty()

# This is the mddle man between the user and the artist it allows them to talk to
#  each other without being stuck to one in particular
class Plus_One(ndb.Model):
    user_key = ndb.KeyProperty(kind=Post)
    artist_key = ndb.KeyProperty(kind=Post)
    like = ndb.BooleanProperty()

class Minus_One(ndb.Model):
    user_key = ndb.KeyProperty(kind=post)
    artist_key = ndb.KeyProperty(kind=post)
    dislike = ndb.BooleanProperty()

# The login landing page
class LoginHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')
        template = jinja_environment.get_template('templates/log_in_page.html')
        self.response.write(template.render())

# We can start this with being a simple about page then change it to be a dinamic
# page that shows artists rankings in wacky categories
class MainHandler(webapp2.RequestHandler):
    def get(self):

        #creating login and logout
        current_user = users.get_current_user()
        login_url = users.create_login_url()
        logout_url = users.create_logout_url()

        template_vars = {
        "current_user": current_user,
        "login_url": login_url,
        "logout_url": logout_url,
        }
        template = jinja_environment.get_template('templates/home.html')
        self.response.write(template.render(template_vars))

# This is the main page where everything happens, the bulk of functionality
class ArtistHandler(webapp2.RequestHandler):
    def get(self):

        template = jinja_environment.get_template('templates/artist_page.html')
        self.response.write(template.render())

# This is the profile page, which is supposed to show you all the stuff in the data base about you
class ProfileHandler(webapp2.RequestHandler):
    def get(self):




        template = jinja_environment.get_template('templates/profile.html')
        self.response.write(template.render())


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/login', LoginHandler),
    ('/artist', ArtistHandler),
    ('/profile',ProfileHandler)
], debug=True)
