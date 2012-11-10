README:

GENERAL OVERVIEW OF FOLDER STRUCTURE htdocs is as follows:
- static 
Contains all the static (non server-side) files associated with web.py framework
- python
Contains all python files, excluding the server file. All modules are kept here too
- templates
Contains the template files used by web.py framework
- web
Contains the web.py modules. DO NOT MODIFY THIS FOLDER


BREAKDOWN OF 'static' FOLDER STRUCTURE
-js 
Contains the custom javascript files for the UI.
-js/jquery
Contains javascript and css files for both the jquery base and jquery UI (including the theme).
Only three files have to be referenced to load all the current jquery base: two js files, one css files. 
Please see index.html for an examples of this.

-css 
Contains the custom styles for the UI. This does NOT include the jquery UI theming css

-img
Contains all the UI images


COMMENTING:
Comments are extremely important in all the code and styles. 
Make sure that everything is indented properly, particularly for html.
Also, in sections, include START and END statements. A complete example of this is as follows:
<html>
    /* START Javascript for loading compass module */
    <script>
    </script>
    /* END Javascript for loading compass module */
    <style>
        head {
            /* Don't include css styles on one line */
            color:blue;
        }
    </style>
</html>
