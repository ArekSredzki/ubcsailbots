#import web.py module
import web
from python.page import *

# Tell web.py where to find all the templates
render = web.template.render('templates/')

# Map our URLs
urls = (
    '/', 'overview',
    '/debug', 'debug',
    '/instructions', 'instructions',
    '/health', 'health',
    '/api', 'api',
    '/shutdown', 'shutdown', 
)

# Declare our classes for the case of each URL mapping
class overview:
    def GET(self):
        page = PageControl()

        page.setTitle('UBC Sailbots - Overview')

        page.addWidget('mapWidget')
        page.addWidget('compassWidget')
        # Note how we are calling 'format' prior to passing the page
        page.format()

        page.navigationBar = render.navigationBar(page)
        page.mapWidget = render.mapWidget(page)
        page.compassWidget = render.compassWidget(page)

        page.contentPane = render.overview(page)
        return render.base(page)

class debug:
    def GET(self):
        page = PageControl()

        page.setTitle('UBC Sailbots - Debug')
        #page.addWidget('map')
        # Note how we are calling 'format' prior to passing the page
        page.format()
        
        page.navigationBar = render.navigationBar(page)
        page.contentPane = render.debug(page)
        return render.base(page)

class instructions:
    def GET(self):
        page = PageControl()

        page.setTitle('UBC Sailbots - Instructions')
        #page.addWidget('map')
        # Note how we are calling 'format' prior to passing the page
        page.format()
        
        page.navigationBar = render.navigationBar(page)
        page.contentPane = render.instructions(page)
        return render.base(page)
class health:
    def GET(self):
        page = PageControl()

        page.setTitle('UBC Sailbots - Boat Health')
        #page.addWidget('map')
        # Note how we are calling 'format' prior to passing the page
        page.format()
        
        page.navigationBar = render.navigationBar(page)
        page.contentPane = render.health(page)
        return render.base(page)

class api:
    def GET(self):
        pass

class shutdown: 
    def GET(self): 
        import sys 
        sys.exit(0)
        
class RequestHandler():
    def POST():
        data = web.data() # you can get data use this method
        
# Run Server Application    
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()