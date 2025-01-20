'''
Classes and functions to load a set of Links and Devices for the 
implementation skeleton (non-normative).
'''
__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm), Brad Kizzort'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
import os.path
import sys
import yaml

from space import log, Restriction
from .DemoParameter import DemoParameter
from .DemoCommand import DemoCommand
from .DemoAsset import DemoAsset

def loadFromYaml(specFile:str | None = None) -> None:
    '''Load the datasets from the optionally specified file name.
    If no file name is specified or the specified file does not exist,
    it will try to load from SpacePythonDataset.yaml in the current working directory
    or the users home directory.
    '''
    # Build the list of paths that could be used to initialize 
    datasetList:list[str] = list()
    if specFile is not None:
        datasetList.append(specFile)
    datasetList.extend(['SpacePythonDataset.yaml', 
                        os.path.expanduser('~/SpacePythonDataset.yaml'),
                        os.path.expanduser('~/.local/data/SpacePythonDataset.yaml'),
                        sys.prefix+'/data/SpacePythonDataset.yaml'])
    # Search the list until an existing file, then open it
    f = None
    for fname in datasetList:
        if os.path.isfile(fname):
            file = open(fname, 'r')
            f = file.read()
            break
    if f is None:
        raise Exception('Could not find dataset SpacePythonDataset.yaml')
    # Add the local type tag constructors
    loader = yaml.SafeLoader(f)
    file.close()

    loader.add_constructor('!SpaceSystem', ss_constructor)
    loader.add_constructor('!GemsDevice', dev_constructor)
    loader.add_constructor('!Restriction', restriction_constructor)
    # Load the datasets
    for item in loader.get_data():
        DemoAsset(item.name, item.pSet, item.cSet)

class SpaceSystem(object):
    def __init__(self, name:str, pSet:dict[str, DemoParameter], cSet:dict[str, DemoCommand]):
        self.name = name
        self.pSet = pSet
        self.cSet = cSet
        
class Device(object):
    def __init__(self, name:str, pSet:dict[str, DemoParameter], cSet:dict[str, DemoCommand]):
        self.name = name
        self.pSet = pSet
        self.cSet = cSet
 
def ss_constructor(loader, node):
    ssMapping = loader.construct_mapping(node, True)
    name = ssMapping['name']
    if name is None:
        log.warning('No mapping to SpaceSystem name')
    ps = ssMapping['ParameterSet']
    if ps is None or len(ps) <=0:
        log.warning('No ParameterSet mapping for {0}'.format(name))
    cs = ssMapping['CommandSet']
    if cs is None or len(cs) <=0:
        log.warning('No CommandSet mapping for {0}'.format(name))
    pSet:dict[str, DemoParameter] = dict()
    for pMap in ps:
        pName = list(pMap.keys())[0]
        defSeq = pMap[pName]
        xp = DemoParameter(pName, defSeq[0], **defSeq[1])
        if pName in pSet:
            log.warning('Duplicate parameter name {0} in {1}'.format(pName, name))
        pSet[pName] = xp
    cSet:dict[str, DemoCommand] = dict()
    for command in cs:
        cName = list(command.keys())[0]
        paramSeq = command[cName]
        args = dict()
        for pMap in paramSeq:
            pName = list(pMap.keys())[0]
            defSeq = pMap[pName]
            p = DemoParameter(pName, defSeq[0], **defSeq[1])
            if pName in args:
                log.warning('Duplicate parameter name {0} in command {1}'.format(pName, cName))
            args[pName] = p
        cmd = DemoCommand(cName, name, args)
        if cName in cSet:
            log.warn('Duplicate command name {0} in {1}'.format(cName, name))
        cSet[cName] = cmd
    return SpaceSystem(name, pSet, cSet)

def dev_constructor(loader, node):
    dev = loader.construct_mapping(node, True)
    name = dev['name']
    if name is None:
        log.warning('No mapping to GemsDevice name')
    ps = dev['ParameterSet']
    if ps is None or len(ps) <=0:
        log.warning('No ParameterSet mapping for {0}'.format(name))
    cs = dev['DirectiveSet']
    if cs is None or len(cs) <=0:
        log.debug('No DirectiveSet mapping for {0}'.format(name))
    pSet:dict[str, DemoParameter] = dict()
    for pMap in ps:
        pName = list(pMap.keys())[0]
        defSeq = pMap[pName]
        xp = DemoParameter(pName, defSeq[0], **defSeq[1])
        if pName in pSet:
            log.warning('Duplicate parameter name {0} in {1}'.format(pName, name))
        pSet[pName] = xp
    cSet:dict[str, DemoCommand] = dict()
    for directive in cs:
        cName = list(directive.keys())[0]
        paramSeq = directive[cName]
        args:dict[str, DemoParameter] = dict()
        for pMap in paramSeq:
            pName = list(pMap.keys())[0]
            defSeq = pMap[pName]
            p = DemoParameter(pName, defSeq[0], **defSeq[1])
            if pName in args:
                log.warning('Duplicate parameter name {0} in directive {1}'.format(pName, cName))
            args[pName] = p
        drct = DemoCommand(cName, name, args)
        if cName in cSet:
            log.warning('Duplicate directive name {0} in {1}'.format(cName, name))
        cSet[cName] = drct
    return Device(name, pSet, cSet)

def restriction_constructor(loader, node):
    tokens = loader.construct_sequence(node, True)
    restrictions:list[Restriction] = list()
    ii = 0
    while ii < len(tokens):
        cls = tokens[ii]
        ii += 1
        res = tokens[ii]
        ii += 1
        cls = cls + 'R'  #Append R to get class name
        constructor = getattr(DemoParameter, cls, None)
        if constructor:
            restrictions.append(constructor(res))
    return restrictions
