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

# -----------
# User Instructions
# 
# Modify the valid_month() function to verify 
# whether the data a user enters is a valid 
# month. If the passed in parameter 'month' 
# is not a valid month, return None. 
# If 'month' is a valid month, then return 
# the name of the month with the first letter 
# capitalized.
#

months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

month_abbvs = dict((m[:3].lower(), m) for m in months)

def valid_month(month):
    if month:
        mabb = month[:3].lower()
        return month_abbvs.get(mabb)

# -----------
# User Instructions
# 
# Modify the valid_day() function to verify 
# whether the string a user enters is a valid 
# day. The valid_day() function takes as 
# input a String, and returns either a valid 
# Int or None. If the passed in String is 
# not a valid day, return None. 
# If it is a valid day, then return 
# the day as an Int, not a String. Don't 
# worry about months of different length. 
# Assume a day is valid if it is a number 
# between 1 and 31.
# Be careful, the input can be any string 
# at all, you don't have any guarantees 
# that the user will input a sensible 
# day.
#
# Hint: The string function isdigit() might be helpful.

def valid_day(day):
    if day.isdigit():
        day_int = int(day)
        if day_int >= 1 and day_int <= 31:
            return day_int

# -----------
# User Instructions
# 
# Modify the valid_year() function to verify 
# whether the string a user enters is a valid 
# year. If the passed in parameter 'year' 
# is not a valid year, return None. 
# If 'year' is a valid year, then return 
# the year as a number. Assume a year 
# is valid if it is a number between 1900 and 
# 2020.
#

def valid_year(year):
    if year and year.isdigit():
        year = int(year)
        if year >= 1900 and year <= 2020:
            return year

# User Instructions
# 
# Implement the function escape_html(s), which replaces
# all instances of:
# > with &gt;
# < with &lt;
# " with &quot;
# & with &amp;
# and returns the escaped string
# Note that your browser will probably automatically 
# render your escaped text as the corresponding symbols, 
# but the grading script will still correctly evaluate it.
# 

def escape_html(s):
    for (k, v) in (('>', '&gt;'),
                 ('<', '&lt;'),
                 ('"', '&quot;'),
                 ('&', '&amp;')):
        s = s.replace(k, v)
    return s
    
form = """
  <form method="post">
    What is your birthday?
    <br>
    <label>Month <input type="text" name="month" value="%(month)s"></label>
    <label>Day <input type="text" name="day" value="%(day)s"></label>
    <label>Year <input type="text" name="year" value="%(year)s"></label>
    <div style="color:red">%(error)s</div>
    <br>
    <br>
    <input type="submit">
  </form>
"""

class MainHandler(webapp2.RequestHandler):
    def write_form(self, error="", month="", day="", year=""):
        self.response.write(form % {"error": error,
                                    "month": escape_html(month),
                                    "day": escape_html(day),
                                    "year": escape_html(year)})
    
    def get(self):
        self.write_form()
    
    def post(self):
        user_month = self.request.get("month")
        user_day = self.request.get("day")
        user_year = self.request.get("year")
        
        month = valid_month(user_month)
        day = valid_day(user_day)
        year = valid_year(user_year)
        
        if not (month and day and year):
            self.write_form("That doesn't look valid to me, friend.",
                            user_month, user_day, user_year)
        else:
            self.redirect("/thanks")
            
class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write("Thanks! That's totally valid day!")
        
    
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/thanks', ThanksHandler)
], debug=True)
