'''
GEMS Directives
'''
__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm), Brad Kizzort'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
from .errors import UnknownParameterError
class GemsDirective(object):    #Normative
    '''
    GEMS directives are similar to spacecraft commands.  There is a directive name
    and a set of parameter=value pairs that can be sent to the GEMS device to change
    device configuration.
    '''
    def __init__(self, name, device, args=dict()):  #Non-normative
        '''
        The Gems Directive constructor is intended for the internal creation
        of a directive catalog.  Use GemsDevice.lookupDirective() to find a 
        catalog entry.
        '''
        self.name   = name
        self.device = device
        self.arg    = args
    def setValues(self, **args):
        '''Set the Parameter values from the Keyword=Value pairs passed
        '''
        params = list(args.keys())
        for param in params:
            if param in self.arg:
                self.arg[param].setValue(args[param])
            else:
                raise UnknownParameterError('GEMS Parameter {0} not defined for {1}'
                                            .format(param, self.name))
    def __repr__(self):
        return "Directive('{0}')".format(self.name)
    def send(self):
        '''Send the directive to the device with the defined parameter values
        '''
        args = dict()
        for argName in list(self.arg.keys()):
            args[argName] = self.arg[argName].value()
        self.device.send(self.name, **args)
