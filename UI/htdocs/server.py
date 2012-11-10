#import web.py module
import web
from python.page import *

render = web.template.render('templates/')

urls = (
    '/', 'index',
    '/shutdown', 'shutdown', 
)

class index:
    def GET(self):
        page = PageControl()
        page.setTitle('UBC Sailbots')
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
        
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()