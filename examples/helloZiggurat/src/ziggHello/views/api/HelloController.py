# HelloController.py
# (C)2013
# Scott Ernst
from pyaid.dict.DictUtils import DictUtils

from pyaid.json.JSON import JSON

from ziggurat.view.api.ApiController import ApiController

#___________________________________________________________________________________________________ HelloController
class HelloController(ApiController):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ echoHello
    def echoHello(self):
        """ An example of a Controller action method. The router (API view instance) is passed in
            for reference and response modification. """

        # Example of modifying the response dictionary directly
        self._router.response['apiInfo'] = ['Hello', 'echoHello']

        # Example of batch modification of the response dictionary
        self._router.addToResponse(
            hello='Ziggurat',
            answer=42,
            question=['The', 'ultimate', 'answer', 'to', 'life'])

#___________________________________________________________________________________________________ echoModel
    def echoModel(self):
        """ An example using a Ziggurat database model. Here a new entry of the ZigguratTest_Test
            model is created and added to the database and its index in differing radices is
            returned in the response.

            NOTE: The model class is imported in-line in this example simply to allow use of the
                Hello Ziggurat examples without model support for those not in an environment
                without the required database support. """

        try:
            from ziggHello.models.zigguratTest.ZigguratTest_Test import ZigguratTest_Test
            model = ZigguratTest_Test.MASTER

            out = dict()
            for name, value in DictUtils.iter(self._router.ziggurat.environ):
                if name.upper() == name:
                    out[name] = StringUtils.toUnicode(value)

            entry = model()
            entry.infoData = out
            model.session.add(entry)
            model.session.flush()
        except Exception as err:
            self._router.response['error'] = str(err)
            self._router.logger.writeError(u'MODEL ERROR', err)
            return

        self._router.response['index'] = [entry.i, entry.i16, entry.i36, entry.i64]
