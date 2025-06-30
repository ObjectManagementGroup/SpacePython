'''
Shell command line parsing of SOLM Parameters
'''
__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm), Brad Kizzort'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
#
import sys
from space import Parameter, MixedParameterValue, NullableMixedParameterValue
from typing import Any
from datetime import datetime
from .parameters import Parameter

class ParserParameter(Parameter):
    '''ParserParameter implements Parameters as used for the procedure execution invoke method.
    '''
    def __init__(self, name:str, dataType:str, **flags:Any):
        '''
        ParserParameter constructor
        
        :param self: Self reference
        :type self:  
        :param name: Parameter name
        :type name: str 
        :param dataType: Data type
        :type dataType: str 
        :param flags: Keywords of flags
        :type flags: Any 
        '''
        self._name = name
        self._type = dataType
        self._value = None

    def value(self) -> NullableMixedParameterValue:
        '''
        Return the current value of the Parameter or None if no value has been 
        reported
        
        :param self: Self reference
        :type self:  
        '''
        return self._value

    def raw(self) -> NullableMixedParameterValue:
        '''Return the current raw value of the Parameter or None if no value has 
        been reported
        
        :param self: Self reference
        :type self:  
        '''
        return self._value

    def name(self) -> str:
        '''Returns the name of the Parameter.
        
        :param self: Self reference
        :type self:  
        '''
        return self._name

    def setValue(self, value:MixedParameterValue):
        '''Set the value of the Parameter, validating against any restrictions. 
        This method will raise an exception if the new value does not meet the 
        restrictions on the Parameter value.
        
        :param self: Self reference
        :type self:  
        :param value: Value
        :type value: MixedParameterValue 
        '''
        self._value = value

    def sample(self) -> dict[str, MixedParameterValue]:
        '''Return a dictionary of information about current sample, including 
        time and values.
        
        :param self: Self reference
        :type self:  
        '''
        return dict()
    
    def type(self) -> str:
        '''Returns the data type of the Parameter.
        
        :param self: Self reference
        :type self:  
        '''
        return self._type

def parseArgs(progname:str, description:str | None='', parameters:list[ParserParameter]=[], args:list[str] | None = None) -> dict[str, MixedParameterValue]:
    '''Parse the input arguments according to the parameter list
    uses sys.argv[1:] if no arguments are supplied.  Returns a
    dictionary object with attributes named after the supplied list
    of parameters.
    
    :param progname: Program name
    :type progname: str 
    :param description: Program description
    :type description: str | None  
    :param parameters: List of application definitions
    :type parameters: list[ParserParameter]
    :param args: List of program arguments
    :type args: list[str] | None
    '''
    if args is None:
        args = sys.argv[1:]
    parser = Parser(progname, description, parameters)
    return parser.parse(args)

#
class Parser(object):
    '''Internal class for command line parse
    '''
    def _int_null(self, arg:NullableMixedParameterValue) -> int:
        '''
        Returns current value of zero if non-numeric
        
        :param self: Self reference
        :type self:  
        :param arg: Input field to cast
        :type arg: NullableMixedParameterValue
        '''
        # handle special case for null
        if arg == None:
            return 0
        if isinstance(arg, datetime):
            return 0
        return int(arg)
    def __init__(self, progname:str, description:str|None, parameters:list[ParserParameter]):
        '''
        Parser constructor
        
        :param self: Self reference
        :type self:  
        :param progname: Program name
        :type progname: str 
        :param description: Program description
        :type description:  
        :param parameters: List of parameters
        :type parameters: list[ParserParameter]
        '''
        self.progname   = progname
        self.description= description
        self.result:dict[str, MixedParameterValue] = dict()
        self.parameters = parameters
        self.parms:dict[str, Parameter] = dict()
        for parm in parameters:
            if parm.value() != None:
                self.result[parm.name()] = self._int_null(parm.value())
            self.parms[parm.name()] = parm
    def parse(self, args:list[str]) -> dict[str, MixedParameterValue]:
        '''
        Performs parsing using provided arguments.
        
        :param self: Self reference
        :type self:  
        :param args: Arguments for parser
        :type args: list[str]
        '''
        positional = True   # Assume the parameters are positional
        index      = 0
        for arg in args:
            if positional and index >= len(self.parms):
                self.error('extra argument %s' % arg)
            if arg.startswith('--'):
                positional = False
                equals = arg.find('=')
                if equals < 0:
                    if arg == '--help':
                        self.print_usage()
                        sys.exit(0)
                    else:
                        argname = arg
                        value   = ''
                else:
                    argname = arg[0:equals]
                    value   = arg[equals+1:]
                name = argname[2:]

                if name in self.parms.keys():
                    self.parseValue(self.parms[name], value)
                else:
                    self.error('unrecognized argument %s' % argname)
            elif positional:
                self.parseValue(self.parameters[index], arg)
                index += 1
            else:
                self.error('cannot use positional after keyword argument')
        self.checkComplete()
        return self.result
    def parseValue(self, parm:Parameter, value:MixedParameterValue):
        '''
        Attempt to apply provided value to provided parameter
        
        :param self: Self reference
        :type self:  
        :param parm: Parameter
        :type parm: Parameter 
        :param value: Value to assign to parameter
        :type value: MixedParameterValue
        '''
        try:
            parm.setValue(value)
        except Exception as e:
            self.error('{0} for {1}'.format(e, parm.name()))
        if parm.value() != None:
            self.result[parm.name()] = self._int_null(parm.value())
    def checkComplete(self):
        '''
        Finalize parsing after parse is completed. Will throw error if required arguments were not provided.
        
        :param self: Self reference
        :type self: 
        '''
        for parm in self.parameters:
            if not parm.name() in self.result:
                self.error('missing parameter %s' % parm.name())
    def usage(self) -> str:
        '''
        Returns application usage information.
        
        :param self: Self reference
        :type self:  
        '''
        guide = self.progname
        for parm in self.parameters:
            guide += ' --%s=<%s>' % (parm.name(), parm.type())
        guide += '\n'
        return guide
    def error(self, message:str) -> None:
        '''
        Outputs error message to standard error.
        
        :param self: Self reference
        :type self:  
        :param message: Error message
        :type message: str 
        '''
        sys.stderr.write(message)
        sys.stderr.write('\n')
        self.print_usage()
        sys.exit(2)
    def print_usage(self) -> None:
        '''
        Outputs application usage and application description to standard error.
        
        :param self: Self reference
        :type self:  
        '''
        sys.stderr.write(self.usage())
        if self.description != None:
            sys.stderr.write(self.description)
