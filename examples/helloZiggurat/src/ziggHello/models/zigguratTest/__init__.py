# __init__.py
# (C)2013
# Scott Ernst

from ziggurat.sqlalchemy.ZigguratModelUtils import ZigguratModelUtils

# Create the database definition for this package and assign it to the DATABASE module variable
DATABASE = ZigguratModelUtils.createDatabaseDefinition(
    name='ziggurattest',
    host='localhost',
    user='ziggtestuser',
    password='password12345')

# Execute the module initialization protocols passing in the local module vars
ZigguratModelUtils.initializeModels(locals())
