from python.page import *

x = PageControl()

x.setTitle("test")
x.addJsInclude("page.js")

x.format()


print x.headBlock