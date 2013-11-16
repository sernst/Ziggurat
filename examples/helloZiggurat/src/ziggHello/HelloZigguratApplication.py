# HelloZigguratApplication.py
# (C)2013
# Scott Ernst

from ziggurat.ZigguratApplication import ZigguratApplication

#___________________________________________________________________________________________________ HelloZigguratApplication
class HelloZigguratApplication(ZigguratApplication):
    """ A hello world example demonstrating the basic of creating a Ziggurat application. """

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ __init__
    def __init__(self, *args, **kwargs):
        """ Creates a new instance of HelloZigguratApplication. """
        super(HelloZigguratApplication, self).__init__(*args, **kwargs)

