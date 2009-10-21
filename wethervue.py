#!/usr/bin/env python2.5

import web
from web import form
from google.appengine.ext import db
from web.contrib.template import render_mako
import data

urls = (
	'/', 'index',
	'/about', 'about',
	'/maps', 'maps',
	'/addMap', 'addMap',
	'/removeMap/(.*)', 'removeMap',
	'/showMap/(.*)', 'showMap',
	'/showMapV3/(.*)', 'showMapV3',
	'/overlays', 'overlays',
	'/addOverlay', 'addOverlay',
	'/removeOverlay/(.*)', 'removeOverlay',
	'/locations', 'locations',	
	'/addAddress', 'addAddress',
	'/removeAddress/(.*)', 'removeAddress'
)


render = render_mako(
        directories=['templates'],
        input_encoding='utf-8',
        output_encoding='utf-8',
        )

app = web.application(urls, globals())

#api key good for localhost only
#GMapsAPIKey = 'ABQIAAAAEd_s8HoCrsRFFcOYL6SdvRT2yXp_ZAY8_ufC3CFXhHIE1NvwkxQb3_ZGfM9R1sRjSfwRGUJudLSTNg'
#api key good for wethervue.appspot.com
GMapsAPIKey = 'ABQIAAAAEd_s8HoCrsRFFcOYL6SdvRQ_VMvLTCA6JbwMdWgByzZEAJwWXRTWDKsZ4oaZNpE0DT92ZqOb5cXJFw'

addressForm = form.Form(
	form.Textbox("street1", class_="validate[required]", description="* Street 1"),
	form.Textbox("street2", description="Street 2"),
	form.Textbox("city", class_="validate[required]", description="* City"),
	form.Textbox("state", class_="validate[required]", description="* State"),
	form.Textbox("zipcode", class_="validate[required]", description="* Zipcode"),
	form.Button("Add Location", type="submit"))

overlayForm = form.Form(
	form.Textbox("description", description="Description"),
	form.Textbox("url", class_="validate[required]", description="* URL"),
	form.Button("Add Overlay", type="submit"))

mapForm = form.Form(
	form.Textbox("name", class_="validate[required]", description="* Name"),
	form.Textbox("description", description="Description"),
	form.Button("Add Map", type="submit"))

class index():
	def GET(self):
		return render.index()
		
def prepareLocationSet():
	locationSet = list(data.getAllLocations())
	for location in locationSet:
		if location.latitude is None:
			data.geocode(location, GMapsAPIKey)

class showMap:
	def GET(self,id):
		prepareLocationSet()
		locationSet = list(data.getAllLocations())
		kmlSet = list(data.getAllOverlays())
		return render.showMap(id=id, locationSet=locationSet, kmlSet=kmlSet)

class showMapV3:
	def GET(self,id):
		prepareLocationSet()
       		locationSet = list(data.getAllLocations())
		kmlSet = list(data.getAllOverlays())
		return render.showMapV3(id=id, locationSet=locationSet, kmlSet=kmlSet)

class locations():
	def GET(self):
		form = addressForm()
		result = data.getAllLocations()
		return render.locations(locationSet=result, form=form)

	def POST(self):
		form = addressForm()
		if not form.validates():
			result = data.getAllLocations()
			return render.locations(locationSet=result, form=form)
		else:
			data.addLocation(form.d, GMapsAPIKey)
			result = data.getAllLocations()
			return render.locations(locationSet=result, form=form)

class maps:
	def GET(self):
		form = mapForm()
		result = data.getAllMaps()
		return render.maps(mapSet=result, form=form)

	def POST(self):
		form = mapForm()
		if not form.validates():
			result = data.getAllMaps()
			return render.maps(mapSet=result, form=form)
		else:
			data.addMap(form.d)
			result = data.getAllMaps()
			return render.maps(mapSet=result, form=form)

class overlays:
	def GET(self):
		form = overlayForm()
		result = data.getAllOverlays()
		return render.overlays(overlaySet=result, form=form)

	def POST(self):
		form = overlayForm()
		if not form.validates():
			result = data.getAllOverlays()
			return render.overlays(overlaySet=result, form=form)
		else:
			data.addOverlay(form.d)
			result = data.getAllOverlays()
			return render.overlays(overlaySet=result, form=form)

class removeAddress:
	def GET(self, id):
		db.delete(id)
		result = data.getAllLocations()
		web.seeother('/locations')

class removeOverlay:
	def GET(self, id):
		db.delete(id)
		result = data.getAllOverlays()
		web.seeother('/overlays')

class removeMap:
	def GET(self, id):
		db.delete(id)
		result = data.getAllMaps()
		web.seeother('/maps')

class about:
	def GET(self):
		return render.about()

if __name__ == '__main__':
	app.cgirun()
