# HelloController.py
# (C)2013
# Scott Ernst

from pyaid.json.JSON import JSON

#___________________________________________________________________________________________________ HelloController
class HelloController(object):
    """A class for..."""

#===================================================================================================
#                                                                                       C L A S S

#___________________________________________________________________________________________________ echoHello
    @classmethod
    def echoHello(cls, router):
        """ An example of a Controller action method. The router (API view instance) is passed in
            for reference and response modification. """

        # Example of modifying the response dictionary directly
        router.response['apiInfo'] = ['Hello', 'echoHello']

        # Example of batch modification of the response dictionary
        router.addToResponse(
            hello='Ziggurat',
            answer=42,
            question=['The', 'ultimate', 'answer', 'to', 'life'])

#___________________________________________________________________________________________________ echoModel
    @classmethod
    def echoModel(cls, router):
        """ An example using a Ziggurat database model. Here a new entry of the ZigguratTest_Test
            model is created and added to the database and its index in differing radices is
            returned in the response.

            NOTE: The model class is imported in-line in this example simply to allow use of the
                Hello Ziggurat examples without model support for those not in an environment
                without the required database support. """

        try:
            from ziggHello.models.ZigguratTest_Test import ZigguratTest_Test
            model = ZigguratTest_Test.MASTER
            entry = model(info=JSON.asString(router.ziggurat.environ))
            model.session.add(entry)
            model.session.flush()
        except Exception, err:
            router.response['error'] = str(err)
            router.logger.writeError(u'MODEL ERROR', err)
            return

        router.reponse['index'] = [entry.i, entry.i16, entry.i36, entry.i64]
