'''
Space Query prompts the operator for inputs.
'''
__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm), Brad Kizzort'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
from abc import ABC, abstractmethod
from importlib import import_module
import os
from typing import Any
from .constants import MixedParameterValue

class SpaceQuery(ABC):  #Normative
    '''
    SpaceQuery provides a common class for displaying prompts for inputs from the operator. 
    Implementations may exist for different ways that procedures may run, such as via a console 
    interface, desktop interface, or web interface.
    '''

    @classmethod
    def instance(cls, module_name:str='') -> 'SpaceQuery':
        '''Returns an instance of the implementing class of provided module name
        or determined based on environment.
        
        :param cls: Class reference
        :type cls:  
        :param module_name: Module name (optional)
        :type module_name: str 
        '''

        # if variable is not provided, default to environment variable
        if module_name == '':
            module_name = os.getenv("SPACEQUERY_DEFAULT_MODULE", 'space.console_queries')

        import_module(module_name)

        for c in SpaceQuery.__subclasses__():
            if(module_name == c.__module__):
                return c()
        
        raise Exception('Factory could not find a suitable SpaceQuery implementation')
    
    @classmethod
    def availableImplementations(cls) -> list[type['SpaceQuery']]:
        '''Returns a list of all known implementations.
        
        :param cls: Description
        :type cls:  
        '''
        return SpaceQuery.__subclasses__()

    @abstractmethod
    def operatorQuery(self, prompt:str='', **parameters:dict[str, MixedParameterValue]) -> dict[str, MixedParameterValue]:
        '''Accepts an optional prompt string and keyword=value pairs.
        If there are no keyword=value pairs, no values will be requested 
        from the operator.  A default value may be supplied for the keyword
        otherwise a value of '' should be used. 
        If no keyword=value pairs are specified and the prompt string is empty, 
        the operator will be asked to continue before returning.
        Returns an space.shell.Namespace object with values provided by the operator
        
        :param self: Self reference
        :type self:  
        :param prompt: Prompt for the interaction
        :type prompt: str 
        :param parameters: Keywords representing each input as part of this prompt interaction
        :type parameters: Any 
        '''
        pass

def spaceQuery(module_name:str='') -> SpaceQuery:
    '''Factory method to provide an implementation of the operatorQuery capability.
    
    :param module_name: Module name (optional)
    :type module_name: str 
    '''
    return SpaceQuery.instance(module_name)

def operatorQuery(prompt:str='', **parameters:Any) -> dict[str, MixedParameterValue]:
    '''Accessor function that provides default implementation of operatorQuery capability.
    
    :param prompt: Prompt for the interaction
    :type prompt: str 
    :param parameters: Keywords representing each input as part of this prompt interaction
    :type parameters: Any 
    '''
    instance = spaceQuery().instance()
    return instance.operatorQuery(prompt, **parameters)
