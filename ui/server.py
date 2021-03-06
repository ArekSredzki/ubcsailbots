#import web.py module
import web
from page import *
import sys
import os
# Tell web.py where to find all the templates

render = web.template.render('templates/')

# Map our URLs
urls = (
    '/', 'overview',
    '/debug', 'debug',
    '/instructions', 'instructions',
    '/api', 'api',
    '/debug/getlog','getlog',
    '/shutdown', 'shutdown',
    '/static', 'static', 
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
        page.contentPane = render.instructions(page)
        return render.base(page)

class api:
    def GET(self):
        i = web.input()
        # CASE of overviewData Request
        try:
            if i.request == 'overviewData':
                return apiControl.getOverviewDataAsJson()
        except:
            #return 'error' is disabled for debug purposes. It is necessary to see the error messages.
            print "Unexpected error:", sys.exc_info()[0]
            raise
        # CASE of instructionsData Request
        try:
            if i.request == 'instructionsData':
                return apiControl.getInstructionsDataAsJson()
        except:
            #return 'error' is disabled for debug purposes. It is necessary to see the error messages
            print "Unexpected error:", sys.exc_info()[0]
            raise
    def POST(self):
        jsonData = web.data()
        print jsonData
        return apiControl.setInstructions(jsonData)
            
        

class getlog:
    def GET(self):
        debugger = apiControl.getDebugMessages();
        return debugger

class shutdown: 
    def GET(self): 
        import sys 
        sys.exit(0)
        
class RequestHandler():
    def POST():
        data = web.data() # you can get data use this method

app = web.application(urls, globals())
