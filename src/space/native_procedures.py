'''
The NativeProcedure class provides support for launching other procedures.
'''
__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm)'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
from .procedures import Procedure
from .constants import MixedParameterValue

class NativeProcedure(Procedure):  #Normative
    '''The NativeProcedure class provides support for launching other procedures.
    '''
    def __init__(self, name:str=''):
        '''
        Constructor for Native Procedures
        
        :param self: Self reference
        :type self:  
        :param name: Name of the procedure
        :type name: str '''
        self._name = name

    def invoke(self, args:dict[str, MixedParameterValue]) -> None:
        '''Method that executes the procedure with provided arguments
        
        :param self: Self reference
        :type self:  
        :param args: Keywords of procedure arguments
        :type args: dict[str, MixedParameterValue]
        '''
        print("Running procedure " + self._name)