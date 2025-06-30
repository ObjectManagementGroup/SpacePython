__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm), Brad Kizzort'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
from space import Command, MixedFlagValue, Parameter, UnknownParameterError, log, MixedParameterValue, Asset
from typing import Any

class DemoCommand(Command):

    def __init__(self, name:str, asset_name:str, args:dict[str, Parameter]):
        self._name = name
        self._asset_name = asset_name
        self._args = args
    
    def setAsset(self, asset:Asset) -> None:
        self._asset = asset

    def setValues(self, **args:Any) -> None:
        print("DemoCommand values set for " + self._name)

        params = list(args.keys())
        for param in params:
            if param in self._args:
                self._args[param].setValue(args[param])                
            else:
                raise UnknownParameterError('Specified command argument {0} not defined for {1}'
                                            .format(param, self.name))
            
        # also update asset values
        newVal:dict[str, MixedParameterValue] = dict()
        for param in params:
            val = self._args[param].value()
            if val != None:
                newVal[param] = val
        self._asset.setParameters(**newVal)

    def __repr__(self):
        return "DemoCommand('{0}')".format(self._name)

    def name(self) -> str:
        return self._name
    
    def send(self, _flags:dict[str, MixedFlagValue]=dict()) -> None:
        log.info('Sending {cmd} to asset {sys}'.format(cmd=self._name, sys=self._asset_name))
        params = list(self._args.keys())
        if len(params) > 0:
            out = '  Command arguments:'
            for param in params:
                out += ' {name}={value}'.format(name=param, value=self._args[param])
            log.info(out) 
            
        if len(_flags) > 0:
            out = '  Command flags:'    
            for flag in list(_flags.keys()):
                out += '  {name}={value}'.format(name=flag, value=_flags[flag])
            log.info(out)
