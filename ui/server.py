#import web.py module
import web
from python.page import *
from python.api import *

# Tell web.py where to find all the templates
render = web.template.render('templates/')

# Map our URLs
urls = (
    '/', 'overview',
    '/debug', 'debug',
    '/instructions', 'instructions',
    '/health', 'health',
    '/api', 'api',
    '/debug/getlog','getlog',
    '/shutdown', 'shutdown', 
)

# Declare our classes for the case of each URL mapping
class overview:
    def GET(self):
        page = PageControl()
        page.setTitle('UBC Sailbots - Overview')
        
        page.addJsInclude('Overview.js');

        page.addWidget('mapWidget')        
        page.addWidget('compassWidget')
        page.addWidget('dataDisplayTableWidget')
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
        page.addJsInclude('debug.js')
        page.addWidget('dataDisplayTableWidget')
        #page.addWidget('map')
        # Note how we are calling 'format' prior to passing the page
        page.format()
        
        page.navigationBar = render.navigationBar(page)
        page.contentPane = render.debug(page)
        return render.base(page)

class instructions:
    def GET(self):
        page = PageControl()
        page.addJsInclude('instructions.js')

        page.setTitle('UBC Sailbots - instructions')
        page.addWidget('dataDisplayTableWidget')
        # Note how we are calling 'format' prior to passing the page
        page.addWidget('mapWidget') 
        page.mapWidget = render.mapWidget(page)
        page.format()
         
        page.navigationBar = render.navigationBar(page)
        page.contentPane = render.Instructions(page)
        return render.base(page)
class health:
    def GET(self):
        page = PageControl()

        page.setTitle('UBC Sailbots - Boat Health')
        page.addWidget('dataDisplayTableWidget')
        # Note how we are calling 'format' prior to passing the page
        page.format()
        
        page.navigationBar = render.navigationBar(page)
        page.contentPane = render.health(page)
        return render.base(page)

class api:
    def GET(self):
        i = web.input()
        # CASE of overviewData Request
        try:
            if i.request == 'overviewData':
                ajaxReturn = ApiControl()
                return ajaxReturn.getOverviewDataAsJson()
        except:
            return 'error'
        
        # CASE of instructionsData Request
        try:
            if i.request == 'instructionsData':
                ajaxReturn = ApiControl()
                return ajaxReturn.getInstructionsDataAsJson()
        except:
            return 'error'
    def POST(self):
        i = web.input()
        
        # to do: handle instructions
        return 'data received' 
        
        

class getlog:
    def GET(self):
        return "Debug Message"

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
