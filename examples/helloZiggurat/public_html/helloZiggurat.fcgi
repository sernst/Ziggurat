#!/user/bin/python
# -*- coding: UTF-8 -*-

# helloZiggurat.fcgi
# (C) 2013
# Scott Ernst

# 1. Append the app's src directory to the python path to make the application available for
#    import within the scope of the current script:
import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)), '..', 'src') ))

# 2. Import the application class you have created for your specific application and instantiate
#    it with assignment to the module variable that will be invoked when the wsgi application is
#    called. The variable for this assignment is usually called 'application' as is used here.
#    The __file__ is passed as an argument to the application constructor, which instructs the
#    application to use the directory where this file resides as the application root path.
from ziggHello.HelloZigguratApplication import HelloZigguratApplication
application = HelloZigguratApplication(__file__)

# 3. Use the Flup WSGIServer to serve and run the Ziggurat application, returning the result to
#    the web server.
from flup.server.fcgi import WSGIServer
WSGIServer(application).run()
