'''
Procedure represents a procedure within the procedure engine.
'''
__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm)'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
from abc import ABC, abstractmethod
from .constants import MixedParameterValue

class Procedure(ABC):  #Normative
    '''Procedure represents a procedure within the procedure engine.
    '''
    @abstractmethod
    def invoke(self, args:dict[str, MixedParameterValue]) -> None:
        '''Invoke the procedure to execute with provided arguments.
        
        :param self: Self reference
        :type self:  
        :param args: Keyword arguments to pass into procedure
        :type args: dict[str, MixedParameterValue] 
        '''
        pass