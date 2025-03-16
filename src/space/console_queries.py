'''
Console Query is an implementation of spaceQuery for command-line input.
'''
__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm)'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
from typing import Any
from .space_queries import SpaceQuery
from .constants import MixedParameterValue

class ConsoleQuery(SpaceQuery):
    '''
    Console Query is an implementation of spaceQuery for command-line input.
    '''

    def operatorQuery(self, prompt:str='', **parameters:Any) -> dict[str, MixedParameterValue]:
        '''Prompts the user for input utilizing a command line prompt.
        
        :param self: Self reference
        :type self:  
        :param prompt: Prompt for the interaction
        :type prompt: str 
        :param parameters: Keywords representing each input as part of this prompt interaction
        :type parameters: Any 
        '''
        res:dict[str, MixedParameterValue] = dict()
        res["result"] = input(prompt + ": ")

        return res
