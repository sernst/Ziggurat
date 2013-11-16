# ZigguratDisplayView.py
# (C)2011-2013
# Scott Ernst and Eric David Wills

from pyaid.ArgsUtils import ArgsUtils
from pyaid.string.StringUtils import StringUtils
from pyaid.web.mako.MakoRenderer import MakoRenderer

from ziggurat.view.ZigguratBaseView import ZigguratBaseView
from ziggurat.view.response.ViewRedirect import ViewRedirect

#___________________________________________________________________________________________________ ZigguratDisplayView
class ZigguratDisplayView(ZigguratBaseView):
    """The abstract base class for all public display entry views."""

#===================================================================================================
#                                                                                       C L A S S

    DEFAULT_CSRF_TOKEN_NAME = 'zigg_csrf'

#___________________________________________________________________________________________________ __init__
    def __init__(self, request, **kwargs):
        """Creates a new instance of ZigguratDisplayView."""
        super(ZigguratDisplayView, self).__init__(request, **kwargs)
        self._minify   = ArgsUtils.get('minify', True, kwargs)
        self._template = ArgsUtils.get('template', None, kwargs)

        self._addCRSFToken()

        self._response = dict(
            request=self._request,
            view=self,
            ziggurat=self.ziggurat )

#===================================================================================================
#                                                                                   G E T / S E T

#___________________________________________________________________________________________________ GS: renderTemplate
    @property
    def template(self):
        if self._template:
            return self._template
        return getattr(self.__class__, 'TEMPLATE', None)
    @template.setter
    def template(self, value):
        self._template = value

#===================================================================================================
#                                                                                     P U B L I C

#___________________________________________________________________________________________________ __call__
    def __call__(self):
        response = ZigguratBaseView.__call__(self)

        try:
            if isinstance(response, dict):
                t = self.template
                if t:
                    mr  = MakoRenderer(
                        template=t,
                        rootPath=self.ziggurat.configurator.makoRootTemplatePath,
                        logger=self.logger,
                        minify=self._minify,
                        data=response)
                    self._request.response.content_type = u'text/html'
                    self._request.response.text = mr.render()
                else:
                    self.logger.write(u'Invalid or missing template: ' + unicode(t))
            else:
                return response
        except Exception, err:
            self.logger.writeError(u'Failed Mako rendering attempt', err)

        # TODO: Should redirect to an error display page if responses are not strings.
        return self._request.response

#===================================================================================================
#                                                                               P R O T E C T E D

#___________________________________________________________________________________________________ _createExplicitResponse
    def _createExplicitResponse(self, responseOverride =None):
        """Doc..."""
        r = responseOverride if responseOverride else self._explicitResponse
        if isinstance(r, ViewRedirect):
            self._renderRedirect(r.url)
            return

        # self._renderRedirect(url)

#___________________________________________________________________________________________________ _addCRSFToken
    def _addCRSFToken(self, tokenName =None):
        name  = tokenName if tokenName else ZigguratDisplayView.DEFAULT_CSRF_TOKEN_NAME
        value = StringUtils.getRandomString(16)
        self._request.response.set_cookie(name, value, overwrite=True)
        self._request.response.set_cookie(
            name + '-secure',
            value,
            secure=True,
            httponly=True,
            overwrite=True)
