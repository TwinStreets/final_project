import webapp2
import os
import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

# This is the user profile
class Profile(ndb.Model):
    name = ndb.StringProperty()
    blurb = ndb.StringProperty()
    email = ndb.StringProperty()
    # liked_artists = ndb.JsonProperty()  # ['artist1', 'artist2']
    # disliked_artists = ndb.JsonProperty()  # ['artist1', 'artist2']

# This is the artist profile
class Artist(ndb.Model):
    name = ndb.StringProperty()
    genre = ndb.StringProperty()
    image = ndb.StringProperty()
    bio = ndb.StringProperty()
    song = ndb.StringProperty()

# This is the mddle man between the user and the artist it allows them to talk to
#  each other without being stuck to one in particular
class Likes(ndb.Model):
    profile_key = ndb.KeyProperty(kind=Profile)
    artist_key = ndb.KeyProperty(kind=Artist)
    like_state = ndb.StringProperty()  # "liked", "disliked", "neither"

# We can start this with being a simple about page then change it to be a dinamic
# page that shows artists rankings in wacky categories
class MainHandler(webapp2.RequestHandler):
    def get(self):

        artist = [ Artist(name='Drake',genre='hip hop',image='https://i.scdn.co/image/cb080366dc8af1fe4dc90c4b9959794794884c66', bio='The best rapper alive', song="https://www.youtube.com/embed/uxpDa-c-4Mc"),
                Artist(name='John Mayer', genre='neo mellow', image='https://i.scdn.co/image/96a2e527431f7bf39cea4bf8702fc8159f08e2aa', bio='Who is this?', song="https://www.youtube.com/embed/7VBex8zbDRs"),
                Artist(name='Logic',genre='rap',image='https://i.scdn.co/image/9aab47129b8405aa80afc5590ed295b7899154f1' , bio = 'An imaginative and stylistically dynamic rap artist who emerged during the early 2010s, Logic launched his career through uploads and independent mixtapes prior to reaching the mainstream with a Def Jam record deal.', song='https://www.youtube.com/embed/yYhTJU4hHkI'),
                Artist(name='"Weird Al" Yankovic ', genre='parody', image='https://i.scdn.co/image/ec2807c3435008760af30c74db264c74e5b27562', bio='This is great', song="https://youtube.com/embed/N9qYF9DZPdw"),
                Artist(name='Amy Winehouse',genre='dance pop ',image='https://i.scdn.co/image/fc4ca9662d2bd129df9d59177f227d2eea723c11', bio='Cool.', song="https://youtube.com/embed/TJAfLE39ZZ8"),
                Artist(name='Chris Brown', genre='R&B', image='https://i.scdn.co/image/97169328b11f362571ae05b2dba51d585fe79615', bio='Where is he?', song="https://youtube.com/embed/Z9eMk051dYg"),
                Artist(name='Kehlani',genre='danse pop',image='https://i.scdn.co/image/322f3e62a60ffd0c3dafa39301abb93ec1f955da', bio='She cool', song="https://youtube.com/embed/LAYgZEMMWxo"),
                Artist(name='Plain White T\'s', genre='pop rock', image='https://i.scdn.co/image/6c5bf3082909c1d4c50341049ac25beb6138f15f', bio='Oh Snap.', song="https://youtube.com/embed/hQlPzrX8u0A"),
                Artist(name='Sky Ferreira',genre='rap',image='https://i.scdn.co/image/d36cc5e3dae9279073c49183359a5d75dbc94f04' , bio = 'The thing', song='https://www.youtube.com/embed/rEamE0MYPkg'),
                Artist(name='"Santana', genre='classic funk rock', image='https://i.scdn.co/image/9d7f889a472b254993c17104d66ac2639177e16c', bio='This is great', song="https://www.youtube.com/embed/nPLV7lGbmT4"),
                Artist(name='Grateful Dead',genre='j pop ',image='https://i.scdn.co/image/bba340d0c2aa4c9cbcbab0a4c3259d8f8e27f0d7', bio='OK?', song="https://youtu.be/embed/pafY6sZt0FE"),
                Artist(name='Maroon 5', genre='dance pop', image='https://i.scdn.co/image/5eb1ba2ee2551e02006a433b4e1ec98075645e9b', bio='Where is he?', song="https://youtube.com/embed/XPpTgCho5ZA"),
                Artist(name='Michael Jackson',genre='pop',image='https://i.scdn.co/image/30bd799d944e3ce9d10b16cf63a0969d145af97f', bio='The best rapper alive', song="https://www.youtube.com/embed/Kr4EQDVETuA"),
                Artist(name='Vanilla Ice', genre='neo mellow', image='https://i.scdn.co/image/d5de5544e245d9a425b28ee231f1c6b2e1f7e089', bio='Who is this?', song="https://www.youtube.com/embed7VBex8zbDRs"),
                Artist(name='Bon Jovi',genre='rap',image='https://i.scdn.co/image/255476a832d9647d73ed03ae51727cb911c565df' , bio = 'The thing', song='https://www.youtube.com/embed/yYhTJU4hHkI'),
                Artist(name='Black Pink', genre='parody', image='https://i.scdn.co/image/a112dc4f7848ef4afd25b40b447963f0e68d413f', bio='This is great', song="https://youtube.com/embed/N9qYF9DZPdw"),
                Artist(name='Taylor Swift',genre='pop',image='https://i.scdn.co/image/04dfc3cd0be270a9a130c9889f154fb39e09fa13', bio='Taylor Swift is that rarest of pop phenomena: a superstar who managed to completely cross over from country to the mainstream.', song="https://www.youtube.com/embed/zIOVMHMNfJ4"),
                Artist(name='Muse', genre='Alternative', image='https://i.scdn.co/image/19ac88c7aec1f68aa6e207aff29efa15d37336a7', bio='Where is he?', song="https://youtube.com/embed/Z9eMk051dYg")]

        artist_query = Artist.query().fetch()

        if not artist_query:
            for a in artist:
                a.put()

        artist_query = Artist.query()
        artists = artist_query.fetch()

# TODO(Kayla) current error we're running into is when new user first logs in, name does not display!!!

        profile=""
        #creating login and logout
        # Should we fetch () the artist info from the query
        current_user = users.get_current_user()
        login_url = users.create_login_url('/')
        logout_url = users.create_logout_url('/')
        if current_user:
            profile = Profile.query().filter(Profile.email == current_user.email()).get()

         # Force the user to log in if they haven't already.
        if not current_user:
            login_url = users.create_login_url('/profile')

        template_vars = {
        "current_user": current_user,
        "login_url": login_url,
        "logout_url": logout_url,
        'artists': artists,
        'profile':profile,

        }


        template = jinja_environment.get_template('templates/home.html')
        self.response.write(template.render(template_vars))
    def post(self):
        email = users.get_current_user().email()

        self.redirect('/')

# This is the main page where everything happens, the bulk of functionality


class ArtistHandler(webapp2.RequestHandler):
    def get(self):


        urlsafe_key2 = self.request.get('key')
        artist_key = ndb.Key(urlsafe=urlsafe_key2)
        artist = artist_key.get()
        current_user = users.get_current_user()
        profile = Profile.query().filter(Profile.email == current_user.email()).get()
        likes_python = Likes.query().filter(ndb.AND(Likes.artist_key == artist_key, Likes.profile_key == profile.key)).get()
        logout_url = users.create_logout_url('/')

        if likes_python == None:
            like_state = 'neither'
        else:
            like_state = likes_python.like_state

        template_vars = {
            'artist':artist,
            # TODO: Get the actual current like_state,
            # or "neither" if there is no Likes object in the database
            # for this user and artist.
            'like_state': like_state, # MADE CHANGE *****
            'logout_url':logout_url
        }

        template = jinja_environment.get_template('templates/artist_page.html')
        self.response.write(template.render(template_vars))

    def post(self):
        pass


# This is the profile page, which is supposed to show you all the stuff in the data base about you
class ProfileHandler(webapp2.RequestHandler):
    def get(self):

        profiles = Profile.query().fetch()
        current_user = users.get_current_user()

        email = current_user.email()
        profile_query = Profile.query().filter(Profile.email == email)
        profile_exists = profile_query.get()

# check for user profile experience
        if not profile_exists:
            template_vars = {
                'profiles': profiles,
                'current_user': current_user,
            }

            template = jinja_environment.get_template('templates/profile.html')
            self.response.write(template.render(template_vars))

        else:
            self.redirect('/')

    def post(self):
        user = users.get_current_user()
        email= user.email()
        name = self.request.get('name')
        blurb = self.request.get('blurb')
        profile = Profile(name=name,blurb=blurb,email=email)
        profile.put()
        self.redirect('/')

class MyProfileHandler(webapp2.RequestHandler):
    def get(self):
        current_user = users.get_current_user()
        logout_url = users.create_logout_url('/')
        profile = Profile.query().filter(Profile.email == current_user.email()).get()
        preferences = Likes.query().fetch()
        likes = Likes.query().filter(Likes.profile_key == profile.key )
        likes = likes.filter(Likes.like_state == 'liked')
        dislikes = Likes.query().filter(Likes.profile_key == profile.key)
        dislikes = dislikes.filter(Likes.like_state == 'disliked' )

        template_vars = {
            'profile': profile,
            'preferences':preferences,
            'likes':likes,
            'dislikes':dislikes,
            'logout_url':logout_url,
        }

        template = jinja_environment.get_template('templates/myprofile.html')
        self.response.write(template.render(template_vars))


class Photo(ndb.Model):
    title = ndb.StringProperty()
    photo_url = ndb.StringProperty()
    like_status = ndb.StringProperty(default=None)
    created = ndb.DateTimeProperty(auto_now_add=True)


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
        # Get information
        artist_key_python = ndb.Key(urlsafe=self.request.get('artist_key'))
        like_button_python = self.request.get('like_button')

        # TODO:
        # 1. Get the current_user, and use it to get the User
        current_user = users.get_current_user()
        profile = Profile.query().filter(Profile.email == current_user.email()).get()
        print "profile", profile
        # 2. Get the Likes model for the User and Artist

        print "artist_key_python", artist_key_python
        print "profile.key", profile.key
        likes_python = Likes.query().filter(ndb.AND(Likes.artist_key == artist_key_python, Likes.profile_key == profile.key)).get()
        print "likes_python", likes_python
        # 3. Add if statements:
        if not likes_python:
            new_likes = Likes(like_state=like_button_python, artist_key=artist_key_python, profile_key=profile.key)
            new_likes.put()
            self.response.write(like_button_python)

        else:
            # Check that the like_button_python and likes_python.like_state are "liked"
            if like_button_python == "liked" and likes_python.like_state == "liked":
                new_like_state = "neither"

            # Check that the like_button_python and likes_python.like_state are "disliked"
            elif like_button_python == "disliked" and likes_python.like_state == "disliked":
                new_like_state = "neither"
            # Check that the like_button_python and likes_python.like_state are different
            else:
                new_like_state = like_button_python

            likes_python.like_state = new_like_state
            likes_python.put()

        # TODO(Thomas): Write back the new like state.
            self.response.write(new_like_state)
class AboutUsHandler(webapp2.RequestHandler):
    def get(self):
        logout_url = users.create_logout_url('/')

        template_vars = {
            'logout_url':logout_url

        }

        template = jinja_environment.get_template('templates/aboutus.html')
        self.response.write(template.render(template_vars))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/artist', ArtistHandler),
    ('/profile', ProfileHandler),
    ('/myprofile', MyProfileHandler),
    ('/photo', PhotoHandler),
    ('/like', LikeHandler),
    ('/aboutus', AboutUsHandler)
], debug=True)
