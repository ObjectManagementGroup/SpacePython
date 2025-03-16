'''
Commands are sent via an Asset
'''
__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm), Brad Kizzort'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
from abc import ABC, abstractmethod
from typing import Any
from .constants import MixedFlagValue

class Command(ABC):  #Normative
    '''
    The Command class incorporates the command name a list of typed
    range-limited arguments.
    '''
    @abstractmethod
    def setValues(self, **args:Any) -> None:
        '''Set the argument values from the Keyword=Value pairs passed
        
        :param self: Self reference
        :type self:  
        :param args: Keywords of command arguments (name=value)
        :type args: Any 
        '''
        pass

    @abstractmethod
    def name(self) -> str:
        '''Returns the name of the command
        
        :param self: Self reference
        :type self:  
        '''
        pass

    @abstractmethod
    def send(self, _flags:dict[str, MixedFlagValue]=dict()) -> None:
        '''Send the command to the asset with the defined argument values
        
        :param self: Self reference
        :type self:  
        :param _flags: Flags for the command (optional)
        :type _flags:  
        '''
        pass
