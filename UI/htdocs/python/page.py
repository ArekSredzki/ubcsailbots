""" Handles all data that is passed to templates. 
* setter/getter methods for page title
* functions for adding javascript and css includes
* functions for adding javascript and css blocks in the <head> section of the html
* addWidget(name) function for adding a widget's js and css files to the web page
* format() function for formatting a public instance variable 'headBlock' which contains formatted HTML for the <head>
* NOTE: not all functions have to be used in all templates. For example, for sub-templates, it is unnecessary to have javascript or css
        file includes, or any <head> or <title> block for that matter. Therefore, while it is good practice to always pass an instance
        of this class to the template, it is not necessary to populate every instance of this class with data, depending on the exact
        use case
*EDITING NOTE: Please make sure you understand how python handles classes before making any edits to this file. Mutable data types in 
        python have to be declared as instance variables and NOT as public variables in global scope. Global scope variables are shared
        between instances and will cause messy results that do not report any errors. 
"""
class PageControl:
    def __init__(self):
        # Declare all public instance variables
        self.headBlock = ''
        self.jsIncludes = []
        self.jsHeadFunctions = []
        self.cssIncludes = []
        self.cssHeadStyles = []
        self.widgets = []
        self.navigationBar = ''
        self.contentPane = ''
        self.mapPane = ''
        
        # Add default Javascript and CSS files for JQuery, JQuery UI and the base css file
        # These files will be included in absolutely every web page as part of the UI
        self.addJsInclude('jquery/js/jquery-1.8.2.js')
        self.addJsInclude('jquery/js/jquery-ui-1.9.1.custom.js')
        self.addJsInclude('base.js')
        
        self.addJsInclude('OpenLayers.js')
        self.addJsInclude('OpenStreetMap.js')
        self.addJsInclude('RenderMap.js')
        
        self.addCssInclude('jquery/css/dark-hive/jquery-ui-1.9.1.custom.css')
        self.addCssInclude('base.css')
        
        self.addCssInclude('map-view.css')
        
    # Declare public variables that are shared across all instances. 
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
    
    # Declare setter/getter methods for the <title> block.
    def setTitle(self, title):
        self.title = title
        
    def getTitle(self):
        return self.title
        
    # Declare methods for adding Javscript or CSS include files. Note that there is no method to remove a file include.
    # Deleting a Javascript or CSS file include can be handled by directly accessing the relevant list, declaring a new instance 
    # OR (preferred method) simply good coding practice of not initially including unnecessary files
    def addJsInclude(self, fileName):
        self.jsIncludes.append('<script src ="/static/js/' + fileName + '"></script>')
    
    def addCssInclude(self, fileName):
        self.cssIncludes.append('<link rel="stylesheet" type="text/css" href="/static/css/' + fileName + '" />')
        
    # Declare methods for adding Javscript or CSS code blocks to the <head>. Note that there is no method to remove code blocks.
    # Deleting a Javascript or CSS code block can be handled by directly accessing the relevant list, declaring a new instance 
    # OR (preferred method) simply good coding practice of not initially adding unnecessary code blocks
    def addJsHeadFunction(self, code):
        self.jsHeadFunctions.append('<script>\n' + code + '\n</script>')
        
    def addCssHeadStyle(self, style):
        self.cssHeadStyles.append('<style>\n' + style + '\n</style>')
    
    # Adds a widget's js and css files to the page
    # Make sure you name your widget files correctly and place them in the 
    # static/css/widgets and static/js/widgets folders. When you pass
    # the 'name' of the widget to this function, don't include the file extension(s)
    def addWidget(self, name):
        self.widgets.append(name)
        
    
    # Formats all the instance data for the <head> block as valid HTML in the 'headBlock' variable.
    def format(self):
        self.jsIncludes = '\n'.join(self.jsIncludes) + '\n'
        self.jsHeadFunctions = '\n'.join(self.jsHeadFunctions) + '\n'
        self.cssIncludes = '\n'.join(self.cssIncludes) + '\n'
        self.cssHeadStyles = '\n'.join(self.cssHeadStyles) + '\n'
        # Include widgets last to ensure that all the jQuery files are already loaded
        for widget in self.widgets[:]:
            self.jsIncludes += '<script src ="static/js/widgets/' + widget + '.js"></script>\n'
            self.cssIncludes += '<link rel="styesheet" type="text/css" href="static/css/widgets/' + widget + '.css" />\n' 
        # Create headBlock 
        self.headBlock = '<title>' + self.title + '</title>\n' + '\n' + self.jsIncludes + '\n' + self.cssIncludes + '\n' + self.jsHeadFunctions + '\n' + self.cssHeadStyles
        

        
    