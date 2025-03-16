'''
This file contains constants and support functions for Space Python.
'''
__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm)'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
from datetime import datetime
from typing import Callable, Any#, Union
from .times import SpecificTime, TimeInterval

FAILED = -1 # Failure
SUCCESSFUL = 0 # Success

# for parameters (and procedure arguments)
type MixedParameterValue = int | float | str | datetime
type NullableMixedParameterValue = MixedParameterValue | None

# for command arguments
type MixedArgumentValue = int | float | str

# for flags
type MixedFlagValue = int | float | str

# unsigned function
def unsigned(value:MixedParameterValue) -> int:
    '''
    Handles conversion of number to an unsigned representation
    
    :param value: Input field
    :type value: MixedParameterValue 
    '''
    # handle specific time being passed into unsigned function
    if isinstance(value, datetime):
        value = 0

    i = int(value)
    if i < 0:
        i = -i
    return i

VALID_PARAMETER_TYPES:dict[str, Any] = { 'boolean': bool, 'byte': int, 'ubyte': unsigned, \
               'short': int, 'ushort': unsigned, 'int': int, \
               'uint': unsigned, 'long': int, 'ulong': unsigned, \
               'float': float, 'double': float, 'string': str, \
               'posixTime': SpecificTime.fromStr, 'hexBitField': int, \
               'uTime': SpecificTime.fromStr, 'interval': TimeInterval.fromStr }

def isSupportedParameterType(type:str) -> bool:
    '''Returns if the provided data type is supported by Space Python.
    
    :param type: Data type
    :type type: str 
    '''
    if VALID_PARAMETER_TYPES.get(type, None) != None:
        return True
    return False

def getParameterFunction(type:str) -> Callable[[Any], Any]:
    '''Returns a conversion function for the provided parameter type.
    Expected to be invoked with a single argument that takes the input data and
    returns the converted value.
    
    :param type: Data Type
    :type type: str 
    '''

    return VALID_PARAMETER_TYPES.get(type, None)