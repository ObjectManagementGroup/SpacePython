'''
SpacePythonException is the base class for all SpacePython
exceptions.  Other exceptions raised by multiple space
modules are defined in this module.
'''
__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm), Brad Kizzort'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
class SpacePythonException(Exception):
    '''Base class for SpacePython exceptions
    '''
    pass
class UnknownParameterError(SpacePythonException):
    '''Named parameter is not defined in this context
    '''
    pass
class TransmissionError(SpacePythonException):  #Normative
    '''Command was not transmitted or receipt was not acknowledged 
    '''
    pass
class VerificationError(SpacePythonException):  #Normative
    '''Command action failed verification telemetry check
    '''
    pass
class GemsError(SpacePythonException):  #Normative
    '''An error occurred accessing a GEMS device
    '''
    pass
class IllegalLinkError(SpacePythonException):  #Normative
    '''The referenced Link does not exist or does not accept commands
    '''
    pass
class UndefinedTypeError(SpacePythonException):  #Normative
    '''The data type of the Parameter is not defined
    for SpacePython parameters.
    '''
    pass
class IllegalValueError(SpacePythonException):  #Normative
    '''The value being assigned to the Parameter is not
    allowed by the data type or value restrictions
    '''
    pass
class QueryCanceledError(SpacePythonException):  #Normative
    ''' The operator canceled the query input.  The script may
    proceed with default values unless a mandatory value is 
    missing.
    '''
    pass
class QueryAbortedError(SpacePythonException):  #Normative
    ''' The operator aborted the procedure during a query 
    operation.  The procedure may catch the abort and exit gracefully
    or, if no try-catch block is active, the procedure should terminate.
    '''
    pass
class VerifyError(SpacePythonException):  #Normative
    '''The verify<expression> procedure step was false.  The procedure
    may catch the exception and continue or halt if no try-catch block
    is active.
    '''
    pass
class TimeoutError(SpacePythonException):  #Normative
    '''Error due to statement timing out rather than completing successfully
    '''

