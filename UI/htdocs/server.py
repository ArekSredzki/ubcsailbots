#import web.py module
import web
render = web.template.render('templates/')

urls = (
    '/', 'index',

)

class index:
    def GET(self):
        return render.base(render.local_tiles())
        
class RequestHandler():
    def POST():
        data = web.data() # you can get data use this method
        
if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()