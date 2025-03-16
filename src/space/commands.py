'''
Commands and CommandRequests may be sent through a Link
'''
__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm), Brad Kizzort'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
from .errors import UnknownParameterError
class Command(object):  #Normative
    '''
    The Command class incorporates the command name a list of typed
    range-limited arguments.
    '''
    def __init__(self, name, link, args=dict()):  #Non-normative
        '''
        The Command constructor is intended for the internal creation
        of the command catalog.  Use Link.lookupCommand() to find a 
        command catalog entry.
        '''
        self.name = name
        self.link = link
        self.arg  = args
    def setValues(self, **args):
        '''Set the argument values from the Keyword=Value pairs passed
        '''
        params = list(args.keys())
        for param in params:
            if param in self.arg:
                self.arg[param].setValue(args[param])
            else:
                raise UnknownParameterError('Specified command argument {0} not defined for {1}'
                                            .format(param, self.name))
    def __repr__(self):
        return "Command('{0}')".format(self.name)
    def send(self, _flags=dict()):
        '''Send the command to the link with the defined argument values
        '''
        args = dict()
        for argName in list(self.arg.keys()):
            args[argName] = self.arg[argName].value()
        self.link.send(self.name, _flags=_flags, **args)
class CommandRequest(object):  #Normative
    '''
    The CommandRequest class incorporates a command and several settable 
    request flags
    '''
    def __init__(self, command): #Flag attribute names are normative, __init__ is not
        '''
        A CommandRequest is constructed from a Command that is returned from 
        the Link.lookupCommand() or Link.commands() methods.
        '''
        self.command = command
        self.releaseAt          = None
        self.preAuthorized      = False
        self.noEncryption       = False
        self.ignoreConstraints  = False
        self.ignoreReceipt      = False
        self.ignoreVerification = False
    def __repr__(self):
        return "CommandRequest('{0}')".format(self.command.name)
    def send(self):
        '''Send this CommandRequest to the Link associated with the Command
        '''
        flags = dict()
        if self.releaseAt is not None:
            flags['releaseAt'] = self.releaseAt
        if self.preAuthorized:
            flags['preAuthorized'] = True
        if self.noEncryption:
            flags['noEncryption'] = True
        if self.ignoreConstraints:
            flags['ignoreConstraints'] = True
        if self.ignoreReceipt:
            flags['ignoreReceipt'] = True
        if self.ignoreVerification:
            flags['ignoreVerification'] = True
        self.command.link.send(self.command.name, _flags=flags)
