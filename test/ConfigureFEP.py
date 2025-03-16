#!/usr/bin/python3
'''
 This SpacePython module provides an example of a spacecraft
 operations procedure that configures a GEMS device and then
 verifies the configuration.
'''
from space import TimeInterval, SpecificTime, GemsDevice
from space import wait, verify, VerifyError, FAILED, SUCCESSFUL
__version__   = '1.1.0'
__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm), Brad Kizzort'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
__scriptname__ = 'ConfigureFEP'
__duration__   = TimeInterval.fromStr(':3.0')
__modified__   = SpecificTime.fromStr('2024-04-25T12:10')
#
def invoke(args):
    '''Configure the Front-End Equipment for a pass.
    '''
#
# Connect to the GEMS Device
    equipment = GemsDevice('FE1')
    syncword  = equipment.lookupParameter('Syncword')
# Set the synchronization pattern
    newPattern = 0xC744
    equipment.send('ChangeSync', Syncword=newPattern)
    wait(2)   # Wait for the change to take effect
    equipment.get(['Syncword'])
    try:
        verify(syncword.value()==newPattern)
        print('Sync pattern is {0:#X}'.format(syncword.value()))
    except VerifyError:
        print('Sync pattern is {0:#X} instead of {1:#X}'\
        .format(syncword.value(), newPattern))
        return FAILED
    return SUCCESSFUL
#
# Boilerplate to allow running as a shell script
__parameters__ = [] 
# If invoked from the command line, configure logger, parse arguments, and invoke
if __name__ == '__main__':
    import logging
    import space
    space.log.setLevel(logging.INFO)
    space.log.addHandler(logging.StreamHandler())
    __args__ = space.parseArgs(__scriptname__,__doc__,__parameters__)
    invoke(__args__)
