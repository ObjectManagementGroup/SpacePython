__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm), Brad Kizzort'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
from space import Asset, Parameter, Command, MixedFlagValue, SpacePythonException, log
from typing import Any
import re
from .DemoParameter import DemoParameter
from .DemoCommand import DemoCommand

class DemoAsset(Asset):

    def __init__(self, name: str, parameters:dict[str, DemoParameter]= dict(), commands:dict[str, DemoCommand] = dict()):
        self._name = name
        self._parameters:dict[str, DemoParameter] = parameters

        for c in list(commands.values()):
            c.setAsset(self)

        self._commands:dict[str, DemoCommand] = commands

        assets_[name] = self

    def lookupParameter(self, parameterName:str) -> Parameter | None:
        if parameterName in self._parameters:
            return self._parameters[parameterName]
        else:
            return None

    def findParameters(self, regexp:str='') -> list[Parameter]:
        keys = list(self._parameters.keys())
        out_list:list[Parameter] = []
        if regexp != '':
            does_it = re.compile(regexp)
            keys = list(filter(does_it.match, keys))

            # build output
            for k in keys:
                out_list.append(self._parameters[k])
        else:
            out_list = list(self._parameters.values())
        return out_list
    
    def updateParameters(self, parameterList:list[str | Parameter]=[]) -> None:
        # This method is expected to cause a poll of the device
        # to get current values.  If parameters are constantly 
        # polled by the ground system, then it is an opportunity
        # to refresh current values for a running script
        if len(parameterList) > 0:
            out = 'Getting {0} parameters:'.format(self._name)
            for param in parameterList:
                out += ' {name}'.format(name=param)
            log.info(out)
        else: 
            raise SpacePythonException('No Parameters specified on updateParameters')

    def setParameters(self, **valueMap:Any) -> None: #dict[str, MixedParameterValue]
        params = list(valueMap.keys())
        if len(params) > 0:
            out = 'Setting {0} parameters:'.format(self._name)
            for param in params:
                out += ' {name}={value}'.format(name=param, value=valueMap[param])
            log.info(out)

            # set value in local table
            for param in params:
                p = self.lookupParameter(param)
                if p != None:
                    p.setValue(valueMap[param])
        else: 
            raise SpacePythonException('No Parameters specified on set')

    def lookupCommand(self, commandName:str) -> Command | None:
        if commandName in self._commands:
            return self._commands[commandName]
        else:
            return None
    
    def findCommands(self, regexp:str='') -> list[Command]:
        keys = list(self._commands.keys())
        out_list:list[Command] = []
        if regexp != '':
            does_it = re.compile(regexp)
            keys = list(filter(does_it.match, keys))

            # build output
            for k in keys:
                out_list.append(self._commands[k])
        else:
            out_list = list(self._commands.values())
        return out_list
    
    def __repr__(self):
        return "Command('{0}')".format(self.name)

    def send(self, command:Command | str, _flags:dict[str, MixedFlagValue]=dict(), **args:Any) -> None:
        cmd = command
        if isinstance(cmd, str):
            cmd_name = cmd
            cmd = self.lookupCommand(cmd)
            if cmd == None:
                raise SpacePythonException('Provided command {0} does not exist'.format(cmd_name))

        if args:
            cmd.setValues(**args)

        cmd.send()

    def name(self) -> str:
        return self._name
    
    def state(self) -> str:
        return "UP"
    
# storage of known assets
assets_:dict[str,DemoAsset] = dict()
