'''
The GemsDevice class is a legacy support class that maps to Asset objects.
'''
__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm)'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
from .assets import Asset
from .space_pythons import spacePython

def GemsDevice(device_name:str) -> Asset:
    '''The GemsDevice function is a legacy support method that creates Asset objects.
    
    :param device_name: Device name
    :type device_name: str 
    '''
    return spacePython().lookupAsset(device_name)
