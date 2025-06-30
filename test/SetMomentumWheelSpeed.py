#!/usr/bin/python3
'''
 This SpacePython module provides an example of a spacecraft
 operations procedure that checks a subsystem state, optionally
 issues a corrective command, and then sends a command to set
 momentum wheel speed based on a change to the current speed.
'''
# The preceding documentation corresponds to the HeaderComment within
# the metamodel.
from space import TimeInterval, SpecificTime, spacePython
from space import SUCCESSFUL, MixedParameterValue, NullableMixedParameterValue, ParserParameter, FAILED
from datetime import datetime
# The following are commonly accepted metadata items for python scripts
# __version__ is required for SpacePython.
# __version__ corresponds to Procedure.version in SOLM
# The other metadata items are optional
__version__   = '1.2.0'
__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm), Brad Kizzort'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
# The following module metadata are SpacePython required elements
# corresponding to Procedure.name, Procedure.duration, and Procedure.lastModified
# in SOLM 
__scriptname__ = 'SetMomentumWheelSpeed'
__duration__   = TimeInterval(0,5) # 5 seconds
__modified__   = SpecificTime.fromStr('2024-11-12T12:00')

def int_null(arg:NullableMixedParameterValue):
    # handle special case for null
    if isinstance(arg, datetime):
        return 0
    if arg == None:
        return 0
    return int(arg)

#
# The invoke function is the required signature for a SpacePython 
# procedure.  It provides a consistency of invocation so that many 
# different procedures with different arguments can be invoked from within 
# an operator GUI.  Rather than the classic Python dict-based 
# variable argument list, SpacePython invoke() uses the Namespace convention
# of a simple object with attributes named with the argument name, for cleaner
# reference syntax
def invoke(args:dict[str, MixedParameterValue]) -> int:
    '''Change the current momentum wheel speed by the positive
       or negative rpm specified by the keyword parameter,
       SpeedIncrement.
    '''
#
# The following boilerplate is not part of the operations 
# procedure, but is required by SpacePython to gain access to Parameters, 
# Commands, and Directives for the spacecraft, control system,
# and equipment managed by the procedure.
    sat1 = spacePython().lookupAsset('SAT1')
    MomentumWheelState = sat1.lookupParameter('MomentumWheelState')
    if MomentumWheelState == None:
        print('MomentumWheelState was not found')
        return FAILED
    MomentumWheelSpeed = sat1.lookupParameter('MomentumWheelSpeed')
    if MomentumWheelSpeed == None:
        print('MomentumWheelSpeed was not found')
        return FAILED
    setWheelSpeed      = sat1.lookupCommand('SetWheelSpeed')
    if setWheelSpeed == None:
        print('SetWheelSpeed was not found')
        return FAILED
#
# The "core" of the procedure example
#
#   If the momentum wheel is off,
#     turn it on 
#   then send the momentum wheel speed control command
#
    if MomentumWheelState.value() == 'Off':
        sat1.send('MomentumWheelOn')        #Simple invocation of named command
#   Set an argument value for Command and send it. 
    if MomentumWheelSpeed.value() != None and not isinstance(args['SpeedIncrement'],datetime):
        setWheelSpeed.setValues(WheelSpeed=(int_null(MomentumWheelSpeed.value()) + int(args['SpeedIncrement'])))
    sat1.send(setWheelSpeed)
    return SUCCESSFUL
#
# End of core procedure
#
# Boilerplate to allow running as a shell script
from space.parameters import MinInclusiveR, MaxInclusiveR
__parameters__:list[ParserParameter] = [ParserParameter('SpeedIncrement', 'int', restriction=[MinInclusiveR(-10000), MaxInclusiveR(10000)])] 
# If invoked from the command line, configure logger, parse arguments, and invoke
if __name__ == '__main__':
    import logging
    import space
    space.log.setLevel(logging.INFO)
    space.log.addHandler(logging.StreamHandler())
    __args__ = space.parseArgs(__scriptname__,__doc__,__parameters__)
    invoke(__args__)

