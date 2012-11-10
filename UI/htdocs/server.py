#import web.py module
import web
from python.page import *

# Tell web.py where to find all the templates
render = web.template.render('templates/')

# Map our URLs
urls = (
    '/', 'index',
    '/debug', 'debug',
    '/instructions', 'instructions',
    '/health', 'health',
    '/shutdown', 'shutdown', 
)

# Declare our classes for the case of each URL mapping
class index:
    def GET(self):
        page = PageControl()

        page.setTitle('UBC Sailbots')
        
        # Note how we are calling 'format' prior to passing the page
        page.format()
        
        page.navigationBar = render.navigationBar(page)
        return render.base(page)

class debug:
    def GET(self):
        page = PageControl()
        page.setTitle('UBC Sailbots - Debug')
        #Note how we are calling 'format' prior to passing the page
        page.format()
        return render.base(page)

class instructions:
    def GET(self):
        page = PageControl()
        page.setTitle('UBC Sailbots - Instructions')
        #Note how we are calling 'format' prior to passing the page
        page.format()
        return render.base(page)

class health:
    def GET(self):
        page = PageControl()
        page.setTitle('UBC Sailbots - Health')
        #Note how we are calling 'format' prior to passing the page
        page.format()
        return render.base(page)


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