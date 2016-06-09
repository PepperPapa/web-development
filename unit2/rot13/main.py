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

def escape_html(s):
    for (k, v) in (('>', '&gt;'),
                 ('<', '&lt;'),
                 ('"', '&quot;'),
                 ('&', '&amp;')):
        s = s.replace(k, v)
    return s

def rot13(s):
    result = []
    for i in s:
        if (ord(i) > 64 and ord(i) < 91):
            start = 65
            result.append(chr(start + (ord(i) + 13 - start) % 26))
        elif (ord(i) > 96 and ord(i) < 123):
            start = 97
            result.append(chr(start + (ord(i) + 13 - start) % 26))
        else:
            result.append(i)
    return "".join(result)

form = """
    <h1>Enter some text to Rot13:</h1>
    <form method="post">
        <textarea name="text" rows="10" cols="60">%(text)s</textarea>
        <br>
        <input type="submit" value="submit">
    </form>
"""

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write(form % {"text": ""})
    
    def post(self):
        user_text = self.request.get("text")
        self.response.write(form % {"text": rot13(user_text)})

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
