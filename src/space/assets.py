'''
Asset represents space and ground assets within the control system.
'''
__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm), Brad Kizzort'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
from abc import ABC, abstractmethod
from typing import Any
from .parameters import Parameter
from .commands import Command
from .constants import MixedFlagValue

class Asset(ABC):  #Normative
    '''
    Asset represents space and ground assets within the control system.
    '''

    @abstractmethod
    def lookupParameter(self, parameterName:str) -> Parameter | None:
        '''Lookup a parameter associated with this Asset
        
        :param self: Self reference
        :type self:  
        :param parameterName: Parameter name
        :type parameterName: str 
        '''
        pass

    @abstractmethod
    def findParameters(self, regexp:str='') -> list[Parameter]:
        '''Return a list of parameters with names passing the regexp filter.
        The default value results in a list of all parameters, which is not 
        recommended due to the potential list size
        
        :param self: Self reference
        :type self:  
        :param regexp: Parameter name regular expression
        :type regexp: str 
        '''
        pass

    @abstractmethod
    def updateParameters(self, parameterList:list[str | Parameter]=[]) -> None:
        '''Refreshes the parameter values. If implementing system always provides
        latest value, this function may be a no-op. Refreshing values does not ensure
        that the value or any aspects of the sample has changed.
        
        :param self: Self reference
        :type self:  
        :param parameterList: List of parameters
        :type parameterList: list[str | Parameter]
        '''
        pass

    @abstractmethod
    def setParameters(self, **valueMap:Any) -> None: #dict[str, MixedParameterValue]
        '''Sets the provided parameters, provided via a dictionary, with key of 
        parameter name and value representing the new finished value.
        
        :param self: Self reference
        :type self:  
        :param valueMap: Keyword arguments of parameters
        :type valueMap: Any
        '''
        pass

    @abstractmethod
    def lookupCommand(self, commandName:str) -> Command | None:
        '''Lookup a command associated with this Asset
        
        :param self: Self reference
        :type self:  
        :param commandName: Command name
        :type commandName: str 
        '''
        pass

    @abstractmethod
    def findCommands(self, regexp:str='') -> list[Command]:
        '''Return a list of commands with names passing the regexp filter.
           The default value results in a list of all commands, which is not
           recommended due to the potential list size.
        
        :param self: Self reference
        :type self:  
        :param regexp: Command name regular expression
        :type regexp: str
        '''
        pass

    @abstractmethod
    def send(self, command:Command | str, _flags:dict[str, MixedFlagValue]=dict(), **args:Any) -> None:
        '''Send a command to the Asset.
        send is called with a command name, flags, and optional keyword=value arguments
        
        :param self: Self reference
        :type self:  
        :param command: Command name or object
        :type command:  
        :param _flags: Flags for the command
        :type _flags:  
        :param args: Keyword of command arguments
        :type args: Any
        '''
        pass

    @abstractmethod
    def name(self) -> str:
        '''Returns the name of the Asset.
        
        :param self: Self reference
        :type self:  
        '''
        pass

    @abstractmethod
    def state(self) -> str:
        '''Return the current state of the Asset.
        
        :param self: Self reference
        :type self:  
        '''
        pass
