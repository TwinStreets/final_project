<<<<<<< HEAD
import webapp2
import os
import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Cheep(ndb.Model):
    message = ndb.StringProperty()
    email = ndb.StringProperty()
    post_time = ndb.DateTimeProperty(auto_now_add=True)

class Cheep(ndb.Model):
    message = ndb.StringProperty()
    email = ndb.StringProperty()
    post_time = ndb.DateTimeProperty(auto_now_add=True)

class LoginHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')
        template = jinja_environment.get_template('templates/log_in_page.html')
        self.response.write(template.render())
=======
#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
>>>>>>> c11aba1d416fb0a1d7c915b79cb2cc76b4e2fcdb

import webapp2
import jinja2
import os
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
