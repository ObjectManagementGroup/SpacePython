'''
Space Python provides functionality to author common procedures that can be executed across multiple control
system software applications.
'''
__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm), Brad Kizzort'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
from abc import ABC, abstractmethod
from importlib import import_module
import os
from .assets import Asset
from .procedure_engines import ProcedureEngine
from .constants import MixedFlagValue

class SpacePython(ABC):  #Normative
    '''
    Space Python provides functionality to author common procedures that can be executed across multiple control
    system software applications. Each control system implements this class and its supporting classes to provide
    integration with their software platform.
    '''

    @abstractmethod
    def lookupAsset(self, name:str) -> Asset:
        '''Look up a parameter via the provided name.
        
        :param self: Self reference
        :type self:  
        :param name: Asset name
        :type name: str 
        '''
        pass

    @abstractmethod
    def findAssets(self, regexp:str='', _flags:dict[str, MixedFlagValue]=dict()) -> list[Asset]:
        '''Return a list of defined SpaceSystems with names passing the regexp filter.
        The default value results in list of all Assets.
        
        :param self: Self reference
        :type self:  
        :param regexp: Regular expression of asset names
        :type regexp: str 
        :param _flags: Flags for the query (optional)
        :type _flags: dict[str, MixedFlagValue]
        '''
        pass

    @abstractmethod
    def procedureEngine(self) -> ProcedureEngine:
        '''Returns implementation of Procedure Engine sub-interface
        
        :param self: Self reference
        :type self:  
        '''
        pass

    @classmethod
    def instance(cls, module_name:str='') -> 'SpacePython':
        '''Returns an instance of the implementing class of provided module name
        or determined based on environment.
        
        :param cls: Class reference
        :type cls:  
        :param module_name: Module name (optional)
        :type module_name: str 
        '''

        # if variable is not provided, default to environment variable
        if module_name == '':
            module_name = os.getenv("SPACEPYTHON_DEFAULT_MODULE", '')

        if module_name == '':
            raise Exception('No default SpacePython module defined via $SPACEPYTHON_DEFAULT_MODULE')

        import_module(module_name)

        for c in SpacePython.__subclasses__():
            if(module_name == c.__module__):
                return c()
        
        raise Exception('Factory could not find a suitable SpacePython implementation')
    
    @classmethod
    def availableImplementations(cls) -> list[type['SpacePython']]:
        '''Returns a list of all known implementations.
        
        :param cls: Class reference
        :type cls:  
        '''
        return SpacePython.__subclasses__()

def spacePython(module_name:str='') -> SpacePython:
    '''Factory method to provide an implementation of Space Python.
    
    :param module_name: Module name (optional)
    :type module_name: str 
    '''
    return SpacePython.instance(module_name)
