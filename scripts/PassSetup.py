#!/usr/bin/python3
'''
 This SpacePython module provides an example of a spacecraft
 operations procedure that queries the operator, invokes a native 
 procedure and waits for an expression to become true.
'''
from space import TimeInterval, SpecificTime, Link, operatorQuery
from space import loadProcedure, TimeoutError, waitFor
from space import SUCCESSFUL, FAILED
__version__   = '1.1.0'
__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm), Brad Kizzort'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
__scriptname__ = 'PassSetup'
__duration__   = TimeInterval.fromStr(':30.0')
__modified__   = SpecificTime.fromStr('2024-04-25T12:10')
#
def invoke(args):
    '''Setup for a pass and wait for Link to come up.
    '''
#
# Invoke the EstablishContact native procedure with the parameter "string"
#  String selection will be default '1' or supplied by operator
    result = operatorQuery('Select RF string for SAT1', string='1')
    establishContact = loadProcedure('EstablishContact')
    establishContact.invoke(result)
# Wait for the link to be established (or timeout)
    sat1 = Link('SAT1')
    try:
        waitFor(lambda:sat1.state()=='UP')
    except TimeoutError:
        print('Timed out waiting for contact')
        return FAILED
    return SUCCESSFUL
#
# Boilerplate to allow running as a shell script, 
__parameters__ = [] 
# If invoked from the command line, configure logger, parse arguments, and invoke
if __name__ == '__main__':
    import logging
    import space
    space.log.setLevel(logging.INFO)
    space.log.addHandler(logging.StreamHandler())
    __args__ = space.parseArgs(__scriptname__,__doc__,__parameters__)
    invoke(__args__)
