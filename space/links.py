'''
The Link and Downlink classes are used to associate with a spacecraft
uplink/downlink and downlink only, respectively.  
'''
__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm), Brad Kizzort'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
import re
from space import log
from .errors import IllegalLinkError
from .commands import CommandRequest
# Create a dictionary for the known links
links_ = dict()

class Link(object):  #Normative
    '''
    The Link class represents an uplink/downlink path for a spaceSystem
    '''
    # Define the Link state list.  Only the first state means that the
    # link is valid (allows commanding and provides telemetry)
    states=['UP', 'DOWN', 'ESTABLISHING']
    
    def __init__(self, spaceSystem):
        '''
        Associate with a Link based on the specified spaceSystem name.
        '''
        # The implementation should validate that the spaceSystem exists
        # and load any necessary data structures to support future 
        # command and telemetry requests.  Link setup/teardown are not
        # necessarily associated with the creation of a Link object, 
        # but are usually performed by native procedures.
        if hasattr(spaceSystem, 'name'):
            self.system = spaceSystem
            links_[spaceSystem.name] = spaceSystem
            self.system.storeLink(self)
        else:
            if spaceSystem in links_:
                self.system = links_[spaceSystem]
            else:
                raise IllegalLinkError('SpaceSystem {0} is not linked'
                                       .format(spaceSystem))
        self.uplink = True
    
    def __repr__(self):
        return "space.Link('{name}')".format(name=self.system.name)
    
    def send(self, command, _flags=dict(), **arguments):
        '''Send a command to the linked spacecraft
        send is called with a command name and optional keyword=value arguments
        '''
        # If this is a Command or CommandRequest, need to use the specific send method
        # to pick up the arguments and flags
        if hasattr(command, 'send'):
            command.send()
        # Should validate the command name, parameter names and values
        # if possible
        else: 
            log.info('Sending {cmd} to spaceSystem {sys}'.format(cmd=command, sys=self.system.name))
            params = list(arguments.keys())
            if len(params) > 0:
                out = '  Command arguments:'
                for param in params:
                    out += ' {name}={value}'.format(name=param, value=arguments[param])
                log.info(out) 
            if len(_flags) > 0:
                out = '  Command flags:'    
                for flag in list(_flags.keys()):
                    out += '  {name}={value}'.format(name=flag, value=_flags[flag])
                log.info(out)
    def lookupParameter(self, name):
        '''Lookup a parameter associated with this Link/spaceSystem
        '''
        if name in self.system.pSet:
            return self.system.pSet[name]
        else:
            return None
     
    def parameters(self, regexp=''):
        '''Return a list of parameters with names passing the regexp filter.
        The default value results in a list of all parameters, which is not 
        recommended due to the potential list size
        '''
        keys = list(self.system.pSet.keys())
        if regexp != '':
            does_it = re.compile(regexp)
            keys = list(filter(does_it.match, keys))
        return keys
    
    def lookupCommand(self, name):
        '''Lookup a command associated with this Link/spaceSystem
        '''
        if name in self.system.cSet:
            return self.system.cSet[name]
        else:
            return None
    
    def commands(self, regexp=''):
        '''Return a list of commands with names passing the regexp filter.
           The default value results in a list of all commands, which is not
           recommended due to the potential list size.
        '''
        keys = list(self.system.cSet.keys())
        if regexp != '':
            does_it = re.compile(regexp)
            keys = list(filter(does_it.match, keys))
        return keys
        
    def createCommandRequest(self, command):
        return CommandRequest(command)

    def state(self):
        '''Return the current state of the Link
        Possible states are defined in states class attribute
        '''
        return 'UP'
    
class Downlink(Link):  #Normative
    '''
    Associate with a Downlink (telemetry only).
    '''
    def __init__(self, spaceSystem):
        Link.__init__(self, spaceSystem)
        self.uplink = False
    
    # Override the methods that are invalid for a Downlink
    def send(self, command, args):
        raise IllegalLinkError('{0} does not support commanding'
                                 .format(self.system.name))
    
    def lookupCommand(self, name):
        raise IllegalLinkError('{0} does not support commanding'
                                 .format(self.system.name))
    
