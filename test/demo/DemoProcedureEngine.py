__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm), Brad Kizzort'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
import re
from space import ProcedureEngine, Procedure
from .DemoProcedure import DemoProcedure

class DemoProcedureEngine(ProcedureEngine):
    procedures_:dict[str,DemoProcedure] = dict()

    def loadProcedure(self, name:str, spaceSystem:str='') -> Procedure:
        return DemoProcedure(name)
    
    def findProcedures(self, regexp:str='', spaceSystem:str='') -> list[Procedure]:
        keys = list(self.procedures_.keys())
        out_list:list[Procedure] = []
        if regexp != '':
            does_it = re.compile(regexp)
            keys = list(filter(does_it.match, keys))

            # build output
            for k in keys:
                out_list.append(self.procedures_[k])
        else:
            out_list = list(self.procedures_.values())
        return out_list
