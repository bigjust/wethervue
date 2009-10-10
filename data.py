import web
from geopy import geocoders
from google.appengine.ext import db

class Map(db.Model):
    name = db.StringProperty()
    description = db.StringProperty()

class Overlay(db.Model):
    description = db.StringProperty()
    url = db.StringProperty()

class Location(db.Model):
    street1 = db.StringProperty()
    street2 = db.StringProperty()
    city = db.StringProperty()
    state = db.StringProperty()
    zipcode = db.StringProperty()
    latitude = db.StringProperty()
    longitude = db.StringProperty()

def addLocation(input, apiKey):
    newLocation = Location()
    newLocation.street1 = input.street1
    newLocation.street2 = input.street2
    newLocation.city = input.city
    newLocation.state = input.state
    newLocation.zipcode = input.zipcode
    geocode(newLocation, apiKey)

def geocode(location, apiKey):
    g = geocoders.Google(apiKey)
    place, (lat, lng) = g.geocode(location.street1 + " " + location.city + " " + location.state + " " + location.zipcode)
    location.latitude=str(lat)
    location.longitude=str(lng)
    location.put()

    
def addOverlay(input):
    newOverlay = Overlay()
    newOverlay.description = input.description
    newOverlay.url = input.url
    newOverlay.put()

def addMap(input):
    newMap = Map()
    newMap.name = input.name
    newMap.description = input.description
    newMap.put()
    
def getAllOverlays():
    return Overlay.all()

def getAllMaps():
    return Map.all()

def getAllLocations():
    return Location.all()
