__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm), Brad Kizzort'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
from space import Procedure, MixedParameterValue, log

class DemoProcedure(Procedure):
    '''Class to emulate a loaded SpacePython module for native procedures
    '''
    def __init__(self, name:str):
        self._name = name

    def invoke(self, args:dict[str, MixedParameterValue]) -> None:
        '''Internal function to log native procedure name and calling arguments
        '''
        log.info('Invoking native procedure {0}'.format(self._name))
        
        logstr = '  with arguments ('
        for name, value in args.items():
            logstr += '{0}={1}'.format(name, value)
        logstr += ')'
        log.info(logstr)