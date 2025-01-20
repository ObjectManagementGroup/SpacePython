#!/usr/bin/python3
'''
 This SpacePython module provides an example of a spacecraft
 operations procedure that checks a subsystem state, optionally
 issues a corrective command, and then sends a command to set
 momentum wheel speed based on a change to the current speed.
'''
# The preceding documentation corresponds to the HeaderComment within
# the metamodel.
from space import TimeInterval, SpecificTime, Link
from space import SUCCESSFUL
# The following are commonly accepted metadata items for python scripts
# __version__ is required for SpacePython.
# __version__ corresponds to Procedure.version in SOLM
# The other metadata items are optional
__version__   = '1.1.0'
__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm), Brad Kizzort'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
# The following module metadata are SpacePython required elements
# corresponding to Procedure.name, Procedure.duration, and Procedure.lastModified
# in SOLM 
__scriptname__ = 'SetMomentumWheelSpeed'
__duration__   = TimeInterval(0,5) # 5 seconds
__modified__   = SpecificTime.fromStr('2024-04-25T12:10')

#
# The invoke function is the required signature for a SpacePython 
# procedure.  It provides a consistency of invocation so that many 
# different procedures with different arguments can be invoked from within 
# an operator GUI.  Rather than the classic Python dict-based 
# variable argument list, SpacePython invoke() uses the Namespace convention
# of a simple object with attributes named with the argument name, for cleaner
# reference syntax
def invoke(args):
    '''Change the current momentum wheel speed by the positive
       or negative rpm specified by the keyword parameter,
       SpeedIncrement.
    '''
#
# The following boilerplate is not part of the operations 
# procedure, but is required by SpacePython to gain access to Parameters, 
# Commands, and Directives for the spacecraft, control system,
# and equipment managed by the procedure.
    sat1 = Link('SAT1')
    MomentumWheelState = sat1.lookupParameter('MomentumWheelState')
    MomentumWheelSpeed = sat1.lookupParameter('MomentumWheelSpeed')
    setWheelSpeed      = sat1.lookupCommand('SetWheelSpeed')
#
# The "core" of the procedure example
#
#   If the momentum wheel is off,
#     turn it on 
#   then send the momentum wheel speed control command
#
    if MomentumWheelState.value() == 'Off':
        sat1.send('MomentumWheelOn')        #Simple invocation of named command
#   Set an argument value for Command from the Link catalog and send it. 
    setWheelSpeed.setValues(WheelSpeed=(MomentumWheelSpeed.value() + args.SpeedIncrement))
    sat1.send(setWheelSpeed)
    return SUCCESSFUL
#
# End of core procedure
#
# Boilerplate to allow running as a shell script
from space.parameters import Parameter, MinInclusiveR, MaxInclusiveR
__parameters__ = [Parameter('SpeedIncrement', 'int', restriction=[MinInclusiveR(-10000), MaxInclusiveR(10000)])] 
# If invoked from the command line, configure logger, parse arguments, and invoke
if __name__ == '__main__':
    import logging
    import space
    space.log.setLevel(logging.INFO)
    space.log.addHandler(logging.StreamHandler())
    __args__ = space.parseArgs(__scriptname__,__doc__,__parameters__)
    invoke(__args__)

