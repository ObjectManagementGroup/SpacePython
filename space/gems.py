'''
The GemsDevice class is used to associate with a specific 
ground equipment.
'''
__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm), Brad Kizzort'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
import re
from space import log
from .errors import GemsError
# Initialize the list of known devices
devices_ = dict()

class GemsDevice:  #Normative
    def __init__(self, device):
        '''
        Establish communication with a ground device.
        '''
        # The implementation should validate that the device exists
        # and load any necessary data structures to support future 
        # get/set/directive requests.    
        if hasattr(device, 'name'):
            self.device = device
            devices_[device.name] = device
        else:
            if device in devices_:
                self.device = devices_[device]
            else:
                raise GemsError('GemsDevice {0} is not defined'.format(device))

    def __repr__(self):
        return "space.GemsDevice('{name}')".format(name=self.device.name)
   
    def get(self, parameters=[]):
        '''get(parameters) refreshes the parameter values by reading from the device
        '''
        # This method is expected to cause a poll of the device
        # to get current values.  If parameters are constantly 
        # polled by the ground system, then it is an opportunity
        # to refresh current values for a running script
        if len(parameters) > 0:
            out = 'Getting {0} parameters:'.format(self.device.name)
            for param in parameters:
                out += ' {name}'.format(name=param)
            log.info(out)
        else: 
            raise GemsError('No Gems Parameters specified on get')
      
    def set(self, **arguments):
        '''Set the value for the parameter=value pairs specified
        '''
        params = list(arguments.keys())
        if len(params) > 0:
            out = 'Setting {0} parameters:'.format(self.device.name)
            for param in params:
                out += ' {name}={value}'.format(name=param, value=arguments[param])
            log.info(out)
        else: 
            raise GemsError('No Gems Parameters specified on set')
   
    def lookupDirective(self, name):
        '''Return a directive with the specified name, if the
        device has a defined directive.
        '''
        if name in self.device.dSet:
            return self.device.dSet[name]
        else:
            return None
   
    def directives(self, regexp=''):
        '''Return a list of directives associated with this
        device and subsystem whose names pass the provided 
        filter.  Default values return all known parameters.
        '''
        keys = list(self.device.dSet.keys())
        if regexp != '':
            does_it = re.compile(regexp)
            keys = list(filter(does_it.match, keys))
        return keys

    def lookupParameter(self, name):
        '''Lookup a parameter associated with this device.
        '''
        if name in self.device.pSet:
            return self.device.pSet[name]
        else:
            return None
   
    def parameters(self, regexp=''):
        '''Return a list of parameters associated with this
        device and subsystem whose names pass the provided 
        filters.  Default values return all known parameters.
        '''
        keys = list(self.device.pSet.keys())
        if regexp != '':
            does_it = re.compile(regexp)
            keys = list(filter(does_it.match, keys))
        return keys
   
    def send(self, directive, **arguments):
        '''Send a directive with the specified parameters to 
        the device
        '''
        # If this is a Directive from the catalog, use the specific send method
        # to pick up the arguments
        if hasattr(directive, 'send'):
            directive.send()
        # Should validate the directive name, parameter names and values
        # if possible
        else: 
            log.info('Sending {dir} to GemsDevice {dev}'.format(dir=directive, dev=self.device.name))
            params = list(arguments.keys())
            if len(params) > 0:
                out = '  Directive parameters:'
                for param in params:
                    out += ' {name}={value}'.format(name=param, value=arguments[param])
                log.info(out) 
