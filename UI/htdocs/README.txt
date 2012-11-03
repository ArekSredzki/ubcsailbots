REAME:

FOLDER STRUCTURE htdocs is as follows:
-jquery
Contains javascript and css files for both the jquery base and jquery UI (including the theme).
Only three files have to be referenced to load all the current jquery base: two js files, one css files. 
Please see index.html for an examples of this.

-css 
Contains the custom styles for the UI. This does NOT include the jquery UI theming css

-js 
Contains the custom javascript files for the UI. This does NOT include the jquery js files.

-images
Contains all the UI images

-templates 
Contains our custom template files which will be loaded by the server based of our base page(s). We 
still need to discuss what type of template language we are going to use, but I suggest that we emulate
something similar to django. 

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
