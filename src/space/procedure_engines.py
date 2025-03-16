'''
Procedure Engines allow for access to procedures and sub-procedures.
'''
__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm), Brad Kizzort'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
from abc import ABC, abstractmethod
from .procedures import Procedure

class ProcedureEngine(ABC):  #Normative
    '''Procedure Engines allow for access to procedures and sub-procedures.
    '''
    @abstractmethod
    def loadProcedure(self, name:str, spaceSystem:str='') -> Procedure:
        '''Loads a named procedure from the procedure catalog.  If spaceSystem
        is provided, spaceSystem-specific procedures will be searched first.
        
        :param self: Self reference
        :type self:  
        :param name: Name of the procedure
        :type name: str 
        :param spaceSystem: Procedure related system
        :type spaceSystem: str 
        '''
        pass

    @abstractmethod
    def findProcedures(self, regexp:str='', spaceSystem:str='') -> list[Procedure]:
        '''Return a list of procedures passing the regexp filter associated
        with the specified SpaceSystem.  The default values return a list 
        of all procedures that are general, i.e., not specific to a 
        SpaceSystem
        
        :param self: Self reference
        :type self:  
        :param regexp: Regular expression of procedure names
        :type regexp: str 
        :param spaceSystem: Procedure related system
        :type spaceSystem: str 
        '''
        pass
