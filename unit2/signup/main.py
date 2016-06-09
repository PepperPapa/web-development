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
import webapp2
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    if not USER_RE.match(username):
        return "username is not valid!"
    return ""

PWD_RE = re.compile(r"^.{3,20}$")
def valid_password(password, verify):
    # TODO: zx valid password and verify can't work!
    if not (PWD_RE.match(password) or
           password != verify):
        return "password is not valid!"
    return ""
    
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    if email and not EMAIL_RE.match(email):
        return "email address is not valid!"
    return ""
    
form = """
  <form method="post">
    <h1>Signup</h1>
    <label style="display: inline-block;
                  width: 320px;
                  text-align: right;">Uername 
        <input type="text" name="username" value="%(username)s">
        <div style="color: red;">%(username_err)s</div>
    </label>
    <br>
    <br>
    <label style="display: inline-block;
                  width: 320px;
                  text-align: right;">Password 
        <input type="password" name="password" value="%(password)s">
    </label>
    <br>
    <br>
    <label style="display: inline-block;
                  width: 320px;
                  text-align: right;">Verify Password 
        <input type="password" name="verify" value="%(verify)s">
        <div style="color:red;">%(verify_err)s</div>
    </label>
    <br>
    <br>
    <label style="display: inline-block;
                  width: 320px;
                  text-align: right;">Email(optional) 
        <input type="text" name="email" value="%(email)s">
        <div style="color:red;">%(email_err)s</div>
    </label>
    <br>
    <br>
    <input type="submit">
  </form>
"""

class MainHandler(webapp2.RequestHandler):
    def write_form(self, username="", password="", verify="", email="",
                         username_err="", verify_err="", email_err=""):
        self.response.write(form % {"username": username,
                                    "password": password,
                                    "verify": verify,
                                    "email": email,
                                    "username_err": username_err,
                                    "verify_err": verify_err,
                                    "email_err": email_err})
        
    def get(self):
        self.write_form()
        
    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")
        
        v_username = valid_username(username)
        v_password = valid_password(password, verify)
        v_email = valid_email(email)
        
        if (v_username or v_password or v_email):
            self.write_form(username = username,
                            email = email,
                            username_err = v_username,
                            verify_err = v_password,
                            email_err = v_email)
        else:
            self.redirect('/welcome')
        
class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("<h1>Welcome," + self.request.get("username") +
                            "</h1>")
    
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
