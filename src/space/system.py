'''
Implements Space Python language functions
'''
__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm), Brad Kizzort'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
import inspect
from .errors import VerifyError

def verify(boolean:bool) -> bool:  #Normative
    '''Verify(boolean)
    Returns True if boolean value is True,
    A False raises an exception which must be caught by procedure
    if the procedure is to continue 
    
    :param boolean: Verification function
    :type boolean: bool 
    '''
    # The reasons for calling verify rather than a simple 
    # if not boolean:
    #     raise Exception
    # is that it allows the TT&C system to log the verification step and
    # provides a short-hand notation  
    frame = inspect.stack()[1]   # Get the stack frame of the caller
    line  = frame[0].f_lineno  # Get the local variables of the caller
    del frame
    if not boolean:
        raise VerifyError('Verify at line %d is False' % line)
    return True