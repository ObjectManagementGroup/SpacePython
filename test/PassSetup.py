#!/usr/bin/python3
'''
 This SpacePython module provides an example of a spacecraft
 operations procedure that queries the operator, invokes a native 
 procedure and waits for an expression to become true.
'''
from space import TimeInterval, SpecificTime, spacePython, operatorQuery
from space import MixedParameterValue, ParserParameter, TimeoutError, waitFor
from space import SUCCESSFUL, FAILED
__version__   = '1.2.0'
__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm), Brad Kizzort'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
__scriptname__ = 'PassSetup'
__duration__   = TimeInterval.fromStr(':30.0')
__modified__   = SpecificTime.fromStr('2024-11-12T12:00')
#
def invoke(arg:dict[str, MixedParameterValue]) -> int:
    '''Setup for a pass and wait for connection to be available.
    '''
#
# Invoke the EstablishContact native procedure with the parameter "string"
#  String selection will be default '1' or supplied by operator
    result:dict[str, MixedParameterValue] = operatorQuery('Select RF string for SAT1', string=1)
    establishContact = spacePython().procedureEngine().loadProcedure('EstablishContact')
    establishContact.invoke(result)
# Wait for the connection to be established (or timeout)
    sat1 = spacePython().lookupAsset('SAT1')
    try:
        waitFor(lambda:sat1.state()=='UP')
    except TimeoutError:
        print('Timed out waiting for contact')
        return FAILED
    return SUCCESSFUL
#
# Boilerplate to allow running as a shell script, 
__parameters__:list[ParserParameter] = [] 
# If invoked from the command line, configure logger, parse arguments, and invoke
if __name__ == '__main__':
    import logging
    import space
    space.log.setLevel(logging.INFO)
    space.log.addHandler(logging.StreamHandler())
    __args__ = space.parseArgs(__scriptname__,__doc__,__parameters__)
    invoke(__args__)
