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
import os
import urllib2
from xml.dom import minidom
from collections import namedtuple
import logging

import webapp2
import jinja2

from google.appengine.api import memcache
from google.appengine.ext import db

DEBUG = os.environ["SERVER_SOFTWARE"].startswith("Development")

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), 
                               autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params);
    
    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

IP_URL = "http://freegeoip.net/xml/"    
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
        """ example xml:
        <Response>
            <IP>4.2.2.2</IP>
            <CountryCode>US</CountryCode>
            <CountryName>United States</CountryName>
            <RegionCode/>
            <RegionName/>
            <City/>
            <ZipCode/>
            <TimeZone/>
            <Latitude>37.751</Latitude>
            <Longitude>-97.822</Longitude>
            <MetroCode>0</MetroCode>
        </Response>
        """
        d = minidom.parseString(content)
        lat = d.getElementsByTagName("Latitude")[0].childNodes[0].nodeValue
        lon = d.getElementsByTagName("Longitude")[0].childNodes[0].nodeValue
        if lat and lon:
            return db.GeoPt(lat, lon)

# make a basic Point class
Point = namedtuple('Point', ["lat", "lon"])
points = [Point(1,2),
          Point(3,4),
          Point(5,6)]

# implement the function gmaps_img(points) that returns the google maps image
# for a map with the points passed in. A example valid response looks like
# this:
#
# http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false&markers=1,2&markers=3,4
#
# Note that you should be able to get the first and second part of an individual Point p with
# p.lat and p.lon, respectively, based on the above code. For example, points[0].lat would 
# return 1, while points[2].lon would return 6.

GMAPS_URL = "http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false&"

def gmaps_img(points):
    markers = "&".join(["markers=%s,%s" % (p.lat, p.lon) for p in points])
    return GMAPS_URL + markers

class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    coords = db.GeoPtProperty()

def top_arts(update = False):
    key = 'top'
    arts = memcache.get(key)
    if arts is None or update:
        logging.error("DB QUERY")
        arts = db.GqlQuery("SELECT * "
                           "FROM Art "
                           "ORDER BY created DESC "
                           "LIMIT 60")
        arts = list(arts)
        memcache.set(key, arts)
    return arts
    
class Mainpage(Handler):
    def render_front(self, title="", art="", error=""):
        arts = top_arts()
        
        # find which arts have coords
        # points = []
        # for art in arts:
        #     if art.coords:
        #         points.append(art.coords)
        # above comment code equals below one statement:
        points = filter(None, (art.coords for art in arts))
        
        # if we have any arts coors, make an image url
        img_url = None
        if points:
            img_url = gmaps_img(points)
            
        # display the image url   
        self.render("front.html", title = title, art = art, error = error, 
                                  arts = arts, img_url = img_url)
        
    def get(self):
        self.render_front()
    
    def post(self):
        title = self.request.get("title")
        art = self.request.get("art")
        
        if title and art:
            # creat instance
            a = Art(title = title, art = art)
            # lookup the user's coordinates from their IP
            coords = get_coords(self.request.remote_addr)
            # if we have coordinates, add them to the Art
            if coords:
                a.coords = coords
            
            # save database
            a.put()
            # return the query and update the cache
            top_arts(True)
            
            # local server can't fresh new post info, you should click fresh 
            # button manually, however cloud server works well
            self.redirect("/")
        else:
            error = "we need both a title and some artwork!"
            self.render_front(title, art, error)
        
app = webapp2.WSGIApplication([
    ('/', Mainpage)
], debug=True)
