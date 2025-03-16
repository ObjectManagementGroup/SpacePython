__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm), Brad Kizzort'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
import re
from space import SpacePython, Asset, ProcedureEngine, MixedFlagValue, IllegalAssetError
from .DemoAsset import assets_
from .DemoProcedureEngine import DemoProcedureEngine

class DemoSpacePython(SpacePython):

    def lookupAsset(self, name:str) -> Asset:
        if name in assets_:
            return assets_[name]
        else:
            raise IllegalAssetError('Asset {0} does not exist'.format(name))

    def findAssets(self, regexp:str='', _flags:dict[str, MixedFlagValue]=dict()) -> list[Asset]:
        keys = list(assets_.keys())
        out_list:list[Asset] = []
        if regexp != '':
            does_it = re.compile(regexp)
            keys = list(filter(does_it.match, keys))

            # build output
            for k in keys:
                out_list.append(assets_[k])
        else:
            out_list = list(assets_.values())
        return out_list

    def procedureEngine(self) -> ProcedureEngine:
        return DemoProcedureEngine()

#def getAssetList() -> dict[str,DemoAsset]:
#    return assets_

#
#  The following code initializes a set of mappings
#  for testing the framework with simple scripts.  This interface is non-normative.
#  It is expected that the framework code will be modified to access the command, telemetry,
#  and equipment lists directly from the ground system software
from . import loader
loader.loadFromYaml()