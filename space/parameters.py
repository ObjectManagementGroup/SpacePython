'''
Parameters are telemetry items for spacecraft and ground equipment or
are items defined by the ground system itself.
'''
__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm), Brad Kizzort'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
import re
from .times import SpecificTime, TimeInterval
from .errors import UndefinedTypeError, IllegalValueError
# define an integer conversion for unsigned types
def unsigned(value):
    i = int(value)  # Let python do all the checking
    if i < 0:
        i = -i
    return i

#
# The typeNames dictionary defines the list of allowed Parameter type names
# and provides a conversion function for each type.    
typeNames = {'boolean': bool,  'byte': int,         'ubyte': unsigned, \
             'short': int,     'ushort': unsigned,  'int': int, \
             'uint': unsigned, 'long': int,        'ulong': unsigned,\
             'float': float,   'double': float,     'string': str,\
             'posixTime': SpecificTime.fromStr,'hexBitField': int,\
             'uTime': SpecificTime.fromStr,    'interval': TimeInterval.fromStr}

class Parameter:  #Normative
    '''Base Class for all ExternalParameter classes in SpacePython
    '''
    def __init__(self, name, dType='double', **kwds):
        '''Create a new Parameter instance
        '''
        self.name = name
        if dType in typeNames:
            self.dType = dType
        else:
            raise UndefinedTypeError('Could not create parameter of data type <{0}>'.format(dType))
        self.description   = None
        self.multiplicity  = None
        self.restriction   = None
        self.units  = None
        self.value_ = None
        self.raw_   = None
        self.time_  = None
        options = list(kwds.keys())
        for option in options:
            if hasattr(self, option):
                setattr(self, option, kwds[option])
    def value(self):
        '''Return the current value of the Parameter or None if no value has been 
        reported
        '''
        # Currently returns a static attribute, but should interface with 
        # the control system to provide the last reported value
        return self.value_
    def raw(self):
        '''Return the current raw value of the Parameter or None if no value has 
        been reported
        '''
        # Currently returns a static attribute, but should interface with 
        # the control system to provide the last reported value
        return self.raw_
    def setValue(self, value):
        '''Set the value of the Parameter, validating against any restrictions. 
        This method will raise an exception if the new value does not meet the 
        restrictions on the Parameter value.
        '''
        # If the value supplied is not of the specified type, try to convert it using the type converter
        value = typeNames[self.dType](value)
        for restriction in self.restriction:
            if not restriction.validate(value):
                raise IllegalValueError('Violates restriction {0}'.format(restriction))
        self.value_ = value
        self.time_  = SpecificTime.now()
    def report(self):
        '''Return a tuple of (value, timestamp) or (None, None) if no reported 
        value
        '''
        return (self.value_, self.time_)
    def __str__(self):
        if self.value_ is not None:
            return str(self.value_)
        else:
            return self.__repr__()
    def __repr__(self):
        r = 'Parameter({0}, dType={1}'.format(self.name, self.dType)
        if self.description is not '':
            r = r + ', description="{0}"'.format(self.description)
        if self.multiplicity is not None:
            r = r + ', multiplicity={0}'.format(self.multiplicity)
        if self.value_ is not None:
            r = r + ', value_={0}'.format(self.value_)
        r = r + ')'
        return r
class GemsParameter(Parameter):  #Normative
    '''Creates a GEMS device parameter
    '''
    def __init__(self, name, device=None, dType='double', **kwds):
        self.device = device #Active device connection for sets/gets
        if 'writable' in kwds:
            self.writable = kwds['writable']
        else:
            self.writable = True 
        Parameter.__init__(self, name, dType, **kwds)
   
class XtceParameter(Parameter):  #Normative
    def __init__(self, name, link=None, dType='double', **kwds):
        self.link = link #Active link for data refresh
        if 'writable' in kwds:
            self.writable = kwds['writable']
        else:
            self.writable = True 
        Parameter.__init__(self, name, dType, **kwds)

class GroundParameter(Parameter):  #Normative
    '''Creates a Ground system parameter
    '''
    def __init__(self, name, dType='double', **kwds):
        if 'writable' in kwds:
            self.writable = kwds['writable']
        else:
            self.writable = True 
        Parameter.__init__(self, name, dType, **kwds)

# Instances of the Restriction can be added to a Parameter so that value changes can be 
# validated
import calendar    #Needed for time conversions
class Restriction(object):
    '''Base class for all value restrictions.
    '''
    def __init__(self):
        pass

class EnumerationR(Restriction):
    '''Limits a string Parameter to a list of values
    '''
    def __init__(self, names=list()):
        self.names = names
    def validate(self, value):
        try:
            self.names.index(value)
            return True
        except:
            return False
    def __repr__(self):
        return 'EnumerationR({0})'.format(self.names)
        
class FractionDigitsR(Restriction):
    '''Restricts the number of digits after the decimal for a float Parameter.
    Not really a limit on the value but could be used to control conversions to 
    and from a string
    '''
    def __init__(self, length):
        self.length = length
    def validate(self, value):
        return True
    def __repr__(self):
        return 'FractionDigitsR({0})'.format(self.length)

class LengthR(Restriction):
    '''Requires a string Parameter to have a specific length
    '''
    def __init__(self, length):
        self.length = length
    def validate(self, value):
        if len(value) == self.length:
            return True
        else:
            return False
    def __repr__(self):
        return 'LengthR({0})'.format(self.length)

class MaxExclusiveR(Restriction):
    '''Requires that an integer or floating parameter be less than a value
    '''
    def __init__(self, maxVal):
        self.maxVal = maxVal
    def validate(self, value):
        if value < self.maxVal:
            return True
        else:
            return False
    def __repr__(self):
        return 'MaxExclusiveR({0})'.format(self.maxVal)

class MaxInclusiveR(Restriction):
    '''Requires that an integer or floating parameter not exceed a value
    '''
    def __init__(self, maxVal):
        self.maxVal = maxVal
    def validate(self, value):
        if value <= self.maxVal:
            return True
        else:
            return False
    def __repr__(self):
        return 'MaxInclusiveR({0})'.format(self.maxVal)

class MaxLengthR(Restriction):
    '''Requires that a string Parameter not exceed a specified length
    '''
    def __init__(self, length):
        self.length = length
    def validate(self, value):
        if len(value) <= self.length:
            return True
        else:
            return False
    def __repr__(self):
        return 'MaxLengthR({0})'.format(self.length)
        
class MaxSecondsExclusiveR(Restriction):
    '''Requires that the seconds portion of a time Parameter not be less than a 
    value
    '''
    def __init__(self, maxVal):
        self.maxVal = maxVal
    def validate(self, value):
        if getattr(value, 'total_seconds', None):
            # TimeInterval and datetime.timedelta will return a total_seconds
            seconds = value.total_seconds()
        else:
            # SpecificTime and datetime.datetime need to be converted to seconds
            tt = value.utctimetuple()
            seconds = calendar.timegm(tt)
        if seconds < self.maxVal:
            return True
        else:
            return False
    def __repr__(self):
        return 'MaxSecondsExclusiveR({0})'.format(self.maxVal)
        
class MaxSecondsInclusiveR(Restriction):
    '''Requires that the nanoseconds portion of a time Parameter not exceed a 
    value
    '''
    def __init__(self, maxVal):
        self.maxVal = maxVal
    def validate(self, value):
        if getattr(value, 'total_seconds', None):
            # TimeInterval and datetime.timedelta will return a total_seconds
            seconds = value.total_seconds()
        else:
            # SpecificTime and datetime.datetime need to be converted to seconds
            tt = value.utctimetuple()
            seconds = calendar.timegm(tt)
        if seconds <= self.maxVal:
            return True
        else:
            return False
    def __repr__(self):
        return 'MaxSecondsInclusiveR({0})'.format(self.maxVal)

class MaxNanosR(Restriction):
    '''Requires that the nanoseconds portion of a time Parameter not exceed a 
    value
    '''
    def __init__(self, maxVal):
        self.maxVal = maxVal
    def validate(self, value):
        if getattr(value, 'nanos', None):
            #SpecificTime and TimeInterval have a nanos() method
            nanos = value.nanos()
        else:
            #datetime.timedelta and datetime.datetime only have microseconds
            nanos = value.microseconds*1000
        if nanos <= self.maxVal:
            return True
        else:
            return False
    def __repr__(self):
        return 'MaxNanosR({0})'.format(self.maxVal)
        
class MinExclusiveR(Restriction):
    '''Requires that an integer or floating parameter be less than a value
    '''
    def __init__(self, minVal):
        self.minVal = minVal
    def validate(self, value):
        if value > self.minVal:
            return True
        else:
            return False
    def __repr__(self):
        return 'MinExclusiveR({0})'.format(self.minVal)

class MinInclusiveR(Restriction):
    '''Requires that an integer or floating parameter not exceed a value
    '''
    def __init__(self, minVal):
        self.minVal = minVal
    def validate(self, value):
        if value >= self.minVal:
            return True
        else:
            return False
    def __repr__(self):
        return 'MinInclusiveR({0})'.format(self.minVal)

class MinLengthR(Restriction):
    '''Requires that a string Parameter not exceed a specified length
    '''
    def __init__(self, length):
        self.length = length
    def validate(self, value):
        if len(value) >= self.length:
            return True
        else:
            return False
    def __repr__(self):
        return 'MinLengthR({0})'.format(self.length)

class MinSecondsExclusiveR(Restriction):
    '''Requires that the seconds portion of a time Parameter not be less than a 
    value
    '''
    def __init__(self, minVal):
        self.minVal = minVal
    def validate(self, value):
        if getattr(value, 'total_seconds', None):
            # TimeInterval and datetime.timedelta will return a total_seconds
            seconds = value.total_seconds()
        else:
            # SpecificTime and datetime.datetime need to be converted to seconds
            tt = value.utctimetuple()
            seconds = calendar.timegm(tt)
        if seconds > self.minVal:
            return True
        else:
            return False
    def __repr__(self):
        return 'MinSecondsExclusiveR({0})'.format(self.minVal)
        
class MinSecondsInclusiveR(Restriction):
    '''Requires that the nanoseconds portion of a time Parameter not exceed a 
    value
    '''
    def __init__(self, minVal):
        self.minVal = minVal
    def validate(self, value):
        if getattr(value, 'total_seconds', None):
            # TimeInterval and datetime.timedelta will return a total_seconds
            seconds = value.total_seconds()
        else:
            # SpecificTime and datetime.datetime need to be converted to seconds
            tt = value.utctimetuple()
            seconds = calendar.timegm(tt)
        if seconds >= self.minVal:
            return True
        else:
            return False
    def __repr__(self):
        return 'MinSecondsInclusiveR({0})'.format(self.minVal)

class MinNanosR(Restriction):
    '''Requires that the nanoseconds portion of a time Parameter not exceed a 
    value
    '''
    def __init__(self, minVal):
        self.minVal = minVal
    def validate(self, value):
        if getattr(value, 'nanos', None):
            #SpecificTime and TimeInterval have a nanos() method
            nanos = value.nanos()
        else:
            #datetime.timedelta and datetime.datetime only have microseconds
            nanos = value.microseconds*1000
        if nanos >= self.minVal:
            return True
        else:
            return False
    def __repr__(self):
        return 'MinNanosR({0})'.format(self.minVal)

class PatternR(Restriction):
    '''Requires that a string Parameter match a specified pattern
    '''
    def __init__(self, pattern):
        self.pattern = pattern
        self.re = re.compile(pattern)
    def validate(self, value):
        if self.re.match(value):
            return True
        else:
            return False
    def __repr__(self):
        return 'PatternR({0})'.format(self.pattern)

class TotalDigitsR(Restriction):
    '''Restricts the total number of digits for a float or integer Parameter.
    Not really a limit on the value but could be used to control conversions to 
    and from a string
    '''
    def __init__(self, maxVal):
        self.maxVal = maxVal
    def validate(self, value):
        return True
    def __repr__(self):
        return 'TotalDigitsR({0})'.format(self.maxVal)
