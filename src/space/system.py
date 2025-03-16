'''
The System module implements the ProcedureEnvironment methods of SOLM
'''
__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm), Brad Kizzort'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
import re
import inspect
#
from space import log
from .times import SpecificTime
from .errors import VerifyError 
from . import loader
from . import links
from . import gems
# SpacePython script return values
FAILED = -1     # Script failure return
SUCCESSFUL = 0  # Script success return

class NativeProcedure(object):
    '''Class to emulate a loaded SpacePython module for native procedures
    '''
    def __init__(self, name='noname', version='1.0.0' ):
        self.__doc__        = 'Native Procedure'
        self.__scriptname__ = name
        self.__version__    = version
        self.__duration__   = None
        self.__modified__   = None
        self.__parser__     = None

    def invoke(self, args):   
        '''Internal function to log native procedure name and calling arguments
        '''
        log.info('Invoking native procedure {0}'.format(self.__scriptname__))
        if args is not None:
            logstr = '  with arguments ('
            for name, value in args.__dict__.items():
                logstr += '{0}={1}'.format(name, value)
            logstr += ')'
            log.info(logstr)

def verify(boolean):  #Normative
    '''Verify(boolean)
    Returns True if boolean value is True,
    A False raises an exception which must be caught by procedure
    if the procedure is to continue 
    '''
    # The reasons for calling verify rather than a simple 
    # if not boolean:
    #     raise Exception
    # is that it allows the TT&C system to log the verification step and
    # provides a short-hand notation  
    frame = inspect.stack()[1]   # Get the stack frame of the caller
    line  = frame[0].f_lineno  # Get the local variables of the caller
    log.info('Verify at line %d is %s' % (line, str(boolean)))
    del frame
    if not boolean:
        raise VerifyError('Verify at line %d is False' % line)
    return True

def now():  #Normative
    '''Return the current time as a SpecificTime
    '''
    return SpecificTime.now()

def today():  #Normative
    '''Return the first valid time of the current day as
    a SpecificTime.  This can be used with TimeIntervals to
    calculate a relative time.
    '''
    return SpecificTime.today()

def lookupParameter(name):  #Normative
    '''Lookup a parameter associated with the control system
    '''
    return None

def parameters(regexp='', subsystem=''):  #Normative
    '''Return a list of control system parameter names with names 
    passing the regexp filter and in the specified subsystem.  The 
    default values result in a list of all parameters, which is not 
    recommended due to the potential list size
    '''
    return []

def links(regexp=''):  #Normative
    '''Return a list of defined SpaceSystems with names passing the regexp filter.
    The default value results in list of all SpaceSystems with telemetry,
    command, and/or procedure definitions.
    '''
    keys = list(links.links_.keys())
    if regexp != '':
        does_it = re.compile(regexp)
        keys = list(filter(does_it.match, keys))
    return keys
        
def activeLinks():  #Normative
    '''Return a dict() of SpaceSystem Links and/or Downlinks that are
    currently active, with SpaceSystem names as keys
    '''
    return links.links_

def equipment(regexp=''):  #Normative
    '''Return a list of GEMS devices with names passing the regexp filter.
    The default value results in a list of all devices.
    '''
    keys = list(gems.devices_.keys())
    if regexp != '':
        does_it = re.compile(regexp)
        keys = list(filter(does_it.match, keys))
    return keys
        
def activeEquipment():  #Normative
    '''Return a dict() of GemsDevice objects that are
    currently active, with the equipment names as keys
    '''
    return gems.devices_

def lookupDirective(name): #Normative
    '''Return the system specific directive with the specified name or None
    '''
    return None
    
def directives(regexp=''):  #Normative
    '''Return a list of control system specific directives passing the 
    regexp filter.  The default value results in a list of all 
    specific directives.
    '''
    return []

def procedures(regexp='', spaceSystem=''):  #Normative
    '''Return a list of procedures passing the regexp filter associated
    with the specified SpaceSystem.  The default values return a list 
    of all procedures that are general, i.e. not specific to a 
    SpaceSystem
    '''
    return []

def loadProcedure(name, spaceSystem=''):  #Normative
    '''Loads a named procedure from the procedure catalog.  If spaceSystem
    is provided, spaceSystem-specific procedures will be searched first 
    '''
#
#  Current implementation only emulates a native procedure execution
#
    return NativeProcedure(name)
    
#
#  The following code initializes a set of mappings
#  for testing the framework with simple scripts.  This interface is non-normative.
#  It is expected that the framework code will be modified to access the command, telemetry,
#  and equipment lists directly from the ground system software

loader.loadFromYaml()
