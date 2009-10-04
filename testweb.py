import web

urls = (
	'/', 'index',
	'/showMap', 'showMap'
)

render = web.template.render('templates/')
app = web.application(urls, globals())

class index:
	def GET(self):
		return render.index()

class showMap:
	def POST(self):
		user_data = web.input(mapID=-1)
		return render.showMap(user_data.mapID)

if __name__ == "__main__": app.run()
