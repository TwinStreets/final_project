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
    user_key = ndb.KeyProperty(kind=User)
    artist_key = ndb.KeyProperty(kind=Artist)
    like = ndb.BooleanProperty()

class Minus_One(ndb.Model):
    user_key = ndb.KeyProperty(kind=User)
    artist_key = ndb.KeyProperty(kind=Artist)
    dislike = ndb.BooleanProperty()

# The login landing page
class LoginHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('templates/log_in_page.html')
        self.response.write(template.render())

# We can start this with being a simple about page then change it to be a dinamic
# page that shows artists rankings in wacky categories
class MainHandler(webapp2.RequestHandler):
    def get(self):

        #creating login and logout
        # Should we fetch () the artist info from the query
        current_user = users.get_current_user()
        login_url = users.create_login_url('/home')
        logout_url = users.create_logout_url('/home')

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

        artist_query = Artist.query()
        artist = artist_query
        template_vars = {
            'artist': artist
        }

        template = jinja_environment.get_template('templates/artist_page.html')
        self.response.write(template.render(template_vars))

    def post(self):

        #like
        # Get inforation
        urlsafe_key1 = self.request.get('user_key')
        urlsafe_key2 = self.request.get('artist_key')
        like = self.request.get('like')
        dislike = self.request.get('dislike')
        # Create an Instance/ interact withb database
        artist_key = ndb.Key(urlsafe=urlsafe_key2)
        user_key = ndb.Key(urlsafe=urlsafe_key1)
        plus_one = Plus_One(user_key=user_key,artist_key=artist_key,like=True)
        minus_one = Minus_One(user_key=user_key,artist_key=artist_key,like=False)
        # Save to database/ create a response
        plus_one.put()
        minus_one.put()
        # Redirect?

        #dislike

# This is the profile page, which is supposed to show you all the stuff in the data base about you
class ProfileHandler(webapp2.RequestHandler):
    def get(self):



        template_vars = {

        }

        template = jinja_environment.get_template('templates/profile.html')
        self.response.write(template.render(template_vars))

class Photo(ndb.Model):
    title = ndb.StringProperty()
    photo_url = ndb.StringProperty()
    like_status = ndb.BooleanProperty(default=None)
    created = ndb.DateTimeProperty(auto_now_add=True)

def add_default_photos():
    # Photo URLs from Wikipedia.
    plus_url = 'https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=0ahUKEwiZp4nhj6XVAhUkrlQKHfNYDPgQjRwIBw&url=https%3A%2F%2Fcommons.wikimedia.org%2Fwiki%2FFile%3AHeart_coraz%25C3%25B3n.svg&psig=AFQjCNHYtKb4FdQzF1E-Vm0F8C0oGXXuAA&ust=1501095799756791'
    minus_url = 'https://www.google.com/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&ved=0ahUKEwiblsTWj6XVAhWCqFQKHUgYCL4QjRwIBw&url=https%3A%2F%2Fcommons.wikimedia.org%2Fwiki%2FFile%3ABroken_heart.svg&psig=AFQjCNFjlfeSot6MUm8J3vODtrBIvUu8DA&ust=1501095756797578'

    plus = Photo(title='Plus', photo_url=plus_url, like_status=None)
    minus = Photo(title='Minus', photo_url=minus_url, like_status=None)

    plus.put()
    minus.put()

    return [plus, minus]

class PhotoHandler(webapp2.RequestHandler):
    def get(self):
        photos = Photo.query().order(-Photo.created).fetch()

        # If there are no photos in the database, add defaults.
        # This will only happen one time (on the first run).
        if not photos:
            photos = add_default_photos()

        template_vars = {
            'photos': photos,
        }

        template = jinja_environment.get_template('templates/artist_page.html')
        self.response.write(template.render(template_vars))

class LikeHandler(webapp2.RequestHandler):
    # Handles increasing the likes when you click the button.
    def post(self):

        # === 1: Get info from the request. ===
        urlsafe_key = self.request.get('photo_key')

        # === 2: Interact with the database. ===

        # Use the URLsafe key to get the photo from the DB.
        photo_key = ndb.Key(urlsafe=urlsafe_key)
        photo = photo_key.get()

        # Fix the photo like count just in case it is None.
        if photo.like_status == False:
            photo.like_status = None

        # Increase the photo count and update the database.
        photo.like_status = True
        photo.put()

        # === 3: Send a response. ===
        # Send the updated count back to the client.
        self.response.write(photo.like_status)

class UnlikeHandler(webapp2.RequestHandler):
    # Handles increasing the likes when you click the button.
    def post(self):

        # === 1: Get info from the request. ===
        urlsafe_key = self.request.get('photo_key')

        # === 2: Interact with the database. ===

        # Use the URLsafe key to get the photo from the DB.
        photo_key = ndb.Key(urlsafe=urlsafe_key)
        photo = photo_key.get()

        # Fix the photo like count just in case it is None.
        if photo.like_status == True:
            photo.like_status = None

        # Increase the photo count and update the database.
        photo.like_status = False
        photo.put()

        # === 3: Send a response. ===
        # Send the updated count back to the client.
        self.response.write(photo.like_status)

app = webapp2.WSGIApplication([
    ('/home', MainHandler),
    ('/', LoginHandler),
    ('/artist', ArtistHandler),
    ('/profile', ProfileHandler),
    ('/photo', PhotoHandler),
], debug=True)
