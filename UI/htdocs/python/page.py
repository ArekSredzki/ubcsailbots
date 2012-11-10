class PageControl:
    def __init__(self):
        #DECLARE all instance variables
        self.headBlock = ''
        self.jsIncludes = []
        self.jsHeadFunctions = []
        self.cssIncludes = []
        self.cssHeadStyles = []
        #add default Javascript and CSS files for JQuery, JQuery UI and the base css file
        self.addJsInclude('static/js/jquery/js/jquery-1.8.2.js')
        self.addJsInclude('static/js/jquery/js/jquery-ui-1.9.1.custom.js')
        self.addJsInclude('static/js/OpenLayers.js')
        self.addJsInclude('static/js/OpenStreetMap.js')
        self.addJsInclude('static/js/RenderMap.js')
        self.addCssInclude('static/js/jquery/css/dark-hive/jquery-ui-1.9.1.custom.css')
        self.addCssInclude('static/css/base.css')
        self.addCssInclude('static/css/map-view.css')
        
    #public variables that are shared across all instances
    title = ''
    
    metaTags = """
        <meta name="author" content="UBC Sailbots Team">
        <link rel="shortcut icon" href="static/img/favicon.ico" type="image/x-icon">
        <meta http-equiv=Content-Type content="text/html; charset="utf-8">
        <meta name=keywords content="sailbots">
        <meta name="description" content="UBC Sailbots Control">
        <meta http-equiv=pragma content=no-cache>
        <meta http-equiv=cache-control content=no-cache>
        <meta http-equiv=expires content=-1>
    """
    
    def setTitle(self, title):
        self.title = title
        
    def getTitle(self):
        return self.title
        
        
    def addJsInclude(self, fileName):
        self.jsIncludes.append('<script src ="' + fileName + '"></script>')
    
    def addCssInclude(self, fileName):
        self.cssIncludes.append('<link rel="styesheet" type="text/css" href="' + fileName + '" />')
        
    def addJsHeadFunction(self, code):
        self.jsHeadFunctions.append('<script>\n' + code + '\n</script>')
        
    def addCssHeadStyle(self, style):
        self.cssHeadStyles.append('<style>\n' + style + '\n</style>')
        
    def format(self):
        self.jsIncludes = '\n'.join(self.jsIncludes) + '\n'
        self.jsHeadFunctions = '\n'.join(self.jsHeadFunctions) + '\n'
        self.cssIncludes = '\n'.join(self.cssIncludes) + '\n'
        self.cssHeadStyles = '\n'.join(self.cssHeadStyles) + '\n'
        self.headBlock = '<title>' + self.title + '</title>\n' + self.metaTags + '\n' + self.jsIncludes + self.cssIncludes + self.jsHeadFunctions + self.cssHeadStyles
        

        
    