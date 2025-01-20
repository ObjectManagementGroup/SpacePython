'''
Parameters are values sampled/known to an Asset or defined within the procedure
language implementation.
'''
__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm), Brad Kizzort'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
from abc import ABC, abstractmethod
from typing import Any
import re
from .times import SpecificTime, TimeInterval
from datetime import datetime, timedelta
import calendar    #Needed for time conversions
from datetime import datetime
from .constants import MixedParameterValue, NullableMixedParameterValue

class Parameter(ABC):  #Normative
    ''' Represents all parameters within SpacePython
    '''
    @abstractmethod
    def value(self) -> NullableMixedParameterValue:
        '''Return the current value of the Parameter or None if no value has been 
        reported
        
        :param self: Self reference
        :type self:  
        '''
        pass

    @abstractmethod
    def raw(self) -> NullableMixedParameterValue:
        '''Return the current raw value of the Parameter or None if no value has 
        been reported
        
        :param self: Self reference
        :type self:  
        '''
        pass

    @abstractmethod
    def name(self) -> str:
        '''Returns the name of the Parameter.
        
        :param self: Self reference
        :type self:  
        '''
        pass

    @abstractmethod
    def setValue(self, value: MixedParameterValue) -> None:
        '''Set the value of the Parameter, validating against any restrictions. 
        This method will raise an exception if the new value does not meet the 
        restrictions on the Parameter value.
        
        :param self: Self reference
        :type self:  
        :param value: Value
        :type value: MixedParameterValue 
        '''
        pass

    @abstractmethod
    def sample(self) -> dict[str, MixedParameterValue]:
        '''Return a dictionary of information about current sample, including 
        time and values.
        
        :param self: Self reference
        :type self:  
        '''
        pass

    @abstractmethod
    def type(self) -> str:
        '''Returns the data type of the Parameter.
        
        :param self: Self reference
        :type self:  
        '''
        pass

# Instances of the Restriction can be added to a Parameter so that value changes can be 
# validated
class Restriction(object):
    '''Base class for all value restrictions.
    '''
    def __init__(self):
        '''
        Restriction constructor
        
        :param self: Self reference
        :type self:  
        '''
        pass

    @abstractmethod
    def validate(self, value:Any) -> bool:
        '''
        Validation function
        
        :param self: Self reference
        :type self:  
        :param value: Input value to check
        :type value: Any
        '''
        pass

class EnumerationR(Restriction):
    '''Limits a string Parameter to a list of values
    '''
    def __init__(self, names:list[str]=list()):
        '''
        Restriction constructor
        
        :param self: Self reference
        :type self:  
        :param names: List of values
        :type names: list[str]
        '''
        self.names = names
    def validate(self, value:str) -> bool:
        '''
        Validation function
        
        :param self: Self reference
        :type self:  
        :param value: Input value to check
        :type value: str 
        '''
        try:
            self.names.index(value)
            return True
        except:
            return False
    def __repr__(self) -> str:
        '''
        Returns class representation
        
        :param self: Self reference
        :type self:  
        '''
        return 'EnumerationR({0})'.format(self.names)
        
class FractionDigitsR(Restriction):
    '''Restricts the number of digits after the decimal for a float Parameter.
    Not really a limit on the value but could be used to control conversions to 
    and from a string
    '''
    def __init__(self, length:int):
        '''
        Restriction constructor
        
        :param self: Self reference
        :type self:  
        :param length: Length limit
        :type length: int 
        '''
        self.length = length
    def validate(self, value: int | float) -> bool:
        '''
        Validation function
        
        :param self: Self reference
        :type self:  
        :param value: Input value to check
        :type value:  
        '''
        return True
    def __repr__(self) -> str:
        '''
        Returns class representation
        
        :param self: Self reference
        :type self:  
        '''
        return 'FractionDigitsR({0})'.format(self.length)

class LengthR(Restriction):
    '''Requires a string Parameter to have a specific length
    '''
    def __init__(self, length:int):
        '''
        Restriction constructor
        
        :param self: Self reference
        :type self:  
        :param length: Numeric length
        :type length: int
        '''
        self.length = length
    def validate(self, value: str) -> bool:
        '''
        Validation function
        
        :param self: Self reference
        :type self:  
        :param value: Input value to check
        :type value: str 
        '''
        if len(value) == self.length:
            return True
        else:
            return False
    def __repr__(self) -> str:
        '''
        Returns class representation
        
        :param self: Self reference
        :type self:  
        '''
        return 'LengthR({0})'.format(self.length)

class MaxExclusiveR(Restriction):
    '''Requires that an integer or floating parameter be less than a value
    '''
    def __init__(self, maxVal: int | float):
        '''
        Restriction constructor
        
        :param self: Self reference
        :type self:  
        :param maxVal: Maximum numeric value
        :type maxVal:  int | float
        '''
        self.maxVal = maxVal
    def validate(self, value: int | float) -> bool:
        '''
        Validation function
        
        :param self: Self reference
        :type self:  
        :param value: Input value to check
        :type value:  
        '''
        if value < self.maxVal:
            return True
        else:
            return False
    def __repr__(self) -> str:
        '''
        Returns class representation
        
        :param self: Self reference
        :type self:  
        '''
        return 'MaxExclusiveR({0})'.format(self.maxVal)

class MaxInclusiveR(Restriction):
    '''Requires that an integer or floating parameter not exceed a value
    '''
    def __init__(self, maxVal:int | float):
        '''
        Restriction constructor
        
        :param self: Self reference
        :type self:  
        :param maxVal: Maximum numeric value
        :type maxVal:  
        '''
        self.maxVal = maxVal
    def validate(self, value:int | float) -> bool:
        '''
        Validation function
        
        :param self: Self reference
        :type self:  
        :param value: Input value to check
        :type value:  
        '''
        if value <= self.maxVal:
            return True
        else:
            return False
    def __repr__(self) -> str:
        '''
        Returns class representation
        
        :param self: Self reference
        :type self:  
        '''
        return 'MaxInclusiveR({0})'.format(self.maxVal)

class MaxLengthR(Restriction):
    '''Requires that a string Parameter not exceed a specified length
    '''
    def __init__(self, length:int):
        '''
        Restriction constructor
        
        :param self: Self reference
        :type self:  
        :param length: Maximum length
        :type length: int 
        '''
        self.length = length
    def validate(self, value:str) -> bool:
        '''
        Validation function
        
        :param self: Self reference
        :type self:  
        :param value: Input value to check
        :type value: str 
        '''
        if len(value) <= self.length:
            return True
        else:
            return False
    def __repr__(self) -> str:
        '''
        Returns class representation
        
        :param self: Self reference
        :type self:  
        '''
        return 'MaxLengthR({0})'.format(self.length)
        
class MaxSecondsExclusiveR(Restriction):
    '''Requires that the seconds portion of a time Parameter not be less than a 
    value
    '''
    def __init__(self, maxVal:int | float):
        '''
        Restriction constructor
        
        :param self: Self reference
        :type self:  
        :param maxVal: Maximum number of seconds
        :type maxVal:  
        '''
        self.maxVal = maxVal
    def validate(self, value:TimeInterval | timedelta | SpecificTime | datetime) -> bool:
        '''
        Validation function
        
        :param self: Self reference
        :type self:  
        :param value: Input value to check
        :type value: TimeInterval | timedelta | SpecificTime | datetime
        '''
        if isinstance(value, TimeInterval) or isinstance(value, timedelta):
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
    def __repr__(self) -> str:
        '''
        Returns class representation
        
        :param self: Self reference
        :type self:  
        '''
        return 'MaxSecondsExclusiveR({0})'.format(self.maxVal)
        
class MaxSecondsInclusiveR(Restriction):
    '''Requires that the nanoseconds portion of a time Parameter not exceed a 
    value
    '''
    def __init__(self, maxVal:int):
        '''
        Restriction constructor
        
        :param self: Self reference
        :type self:  
        :param maxVal: Maxiumum nanoseconds value
        :type maxVal: int 
        '''
        self.maxVal = maxVal
    def validate(self, value:TimeInterval | timedelta | SpecificTime | datetime) -> bool:
        '''
        Validation function
        
        :param self: Self reference
        :type self:  
        :param value: Input value to check
        :type value: TimeInterval | timedelta | SpecificTime | datetime
        '''
        if isinstance(value, TimeInterval) or isinstance(value, timedelta):
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
    def __repr__(self) -> str:
        '''
        Returns class representation
        
        :param self: Self reference
        :type self:  
        '''
        return 'MaxSecondsInclusiveR({0})'.format(self.maxVal)

class MaxNanosR(Restriction):
    '''Requires that the nanoseconds portion of a time Parameter not exceed a 
    value
    '''
    def __init__(self, maxVal:int):
        '''
        Restriction constructor
        
        :param self: Self reference
        :type self:  
        :param maxVal: Maximum nanoseconds value
        :type maxVal: int 
        '''
        self.maxVal = maxVal
    def validate(self, value:TimeInterval | timedelta | SpecificTime | datetime) -> bool:
        '''
        Validation function
        
        :param self: Self reference
        :type self:  
        :param value: Input value to check
        :type value: TimeInterval | timedelta | SpecificTime | datetime
        '''
        if isinstance(value, SpecificTime) or isinstance(value, TimeInterval):
            #SpecificTime and TimeInterval have a nanos() method
            nanos = value.nanos()
        elif isinstance(value, timedelta):
            #datetime.timedelta has microseconds
            nanos = value.microseconds*1000
        else:
            #datetime.datetime has microsecond
            nanos = value.microsecond*1000
        if nanos <= self.maxVal:
            return True
        else:
            return False
    def __repr__(self) -> str:
        '''
        Returns class representation
        
        :param self: Self reference
        :type self:  
        '''
        return 'MaxNanosR({0})'.format(self.maxVal)
        
class MinExclusiveR(Restriction):
    '''Requires that an integer or floating parameter be less than a value
    '''
    def __init__(self, minVal:int | float):
        '''
        Restriction constructor
        
        :param self: Self reference
        :type self:  
        :param minVal: Minimum value
        :type minVal: int | float 
        '''
        self.minVal = minVal
    def validate(self, value:int | float) -> bool:
        '''
        Validation function
        
        :param self: Self reference
        :type self:  
        :param value: Input value to check
        :type value: int | float 
        '''
        if value > self.minVal:
            return True
        else:
            return False
    def __repr__(self) -> str:
        '''
        Returns class representation
        
        :param self: Self reference
        :type self:  
        '''
        return 'MinExclusiveR({0})'.format(self.minVal)

class MinInclusiveR(Restriction):
    '''Requires that an integer or floating parameter not exceed a value
    '''
    def __init__(self, minVal:int | float):
        '''
        Restriction constructor
        
        :param self: Self reference
        :type self:  
        :param minVal: Minimum value
        :type minVal: int | float
        '''
        self.minVal = minVal
    def validate(self, value:int | float) -> bool:
        '''
        Validation function
        
        :param self: Self reference
        :type self:  
        :param value: Input value to check
        :type value: int | float
        '''
        if value >= self.minVal:
            return True
        else:
            return False
    def __repr__(self) -> str:
        '''
        Returns class representation
        
        :param self: Self reference
        :type self:  
        '''
        return 'MinInclusiveR({0})'.format(self.minVal)

class MinLengthR(Restriction):
    '''Requires that a string Parameter not exceed a specified length
    '''
    def __init__(self, length:int):
        '''
        Restriction constructor
        
        :param self: Self reference
        :type self:  
        :param length: Minimum string length
        :type length: int 
        '''
        self.length = length
    def validate(self, value:str) -> bool:
        '''
        Validation function
        
        :param self: Self reference
        :type self:  
        :param value: Input value to check
        :type value: str 
        '''
        if len(value) >= self.length:
            return True
        else:
            return False
    def __repr__(self) -> str:
        '''
        Returns class representation
        
        :param self: Self reference
        :type self:  
        '''
        return 'MinLengthR({0})'.format(self.length)

class MinSecondsExclusiveR(Restriction):
    '''Requires that the seconds portion of a time Parameter not be less than a 
    value
    '''
    def __init__(self, minVal:int):
        '''
        Restriction constructor
        
        :param self: Self reference
        :type self:  
        :param minVal: Minimum seconds
        :type minVal: int '''
        self.minVal = minVal
    def validate(self, value:TimeInterval | timedelta | SpecificTime | datetime) -> bool:
        '''
        Validation function
        
        :param self: Self reference
        :type self:  
        :param value: Input value to check
        :type value: TimeInterval | timedelta | SpecificTime | datetime
        '''
        if isinstance(value, TimeInterval) or isinstance(value, timedelta):
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
    def __repr__(self) -> str:
        '''
        Returns class representation
        
        :param self: Self reference
        :type self:  
        '''
        return 'MinSecondsExclusiveR({0})'.format(self.minVal)
        
class MinSecondsInclusiveR(Restriction):
    '''Requires that the nanoseconds portion of a time Parameter not exceed a 
    value
    '''
    def __init__(self, minVal:int):
        '''
        Restriction constructor
        
        :param self: Self reference
        :type self:  
        :param minVal: Minimums seconds
        :type minVal: int 
        '''
        self.minVal = minVal
    def validate(self, value:TimeInterval | timedelta | SpecificTime | datetime) -> bool:
        '''
        Validation function
        
        :param self: Self reference
        :type self:  
        :param value: Input value to check
        :type value: TimeInterval | timedelta | SpecificTime | datetime
        '''
        if isinstance(value, TimeInterval) or isinstance(value, timedelta):
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
    def __repr__(self) -> str:
        '''
        Returns class representation
        
        :param self: Self reference
        :type self:  
        '''
        return 'MinSecondsInclusiveR({0})'.format(self.minVal)

class MinNanosR(Restriction):
    '''Requires that the nanoseconds portion of a time Parameter not exceed a 
    value
    '''
    def __init__(self, minVal:int):
        '''
        Restriction constructor
        
        :param self: Self reference
        :type self:  
        :param minVal: Minimum nanoseconds value
        :type minVal: int
        '''
        self.minVal = minVal
    def validate(self, value:TimeInterval | timedelta | SpecificTime | datetime) -> bool:
        '''
        Validation function
        
        :param self: Self reference
        :type self:  
        :param value: Input value to check
        :type value: TimeInterval | timedelta | SpecificTime | datetime
        '''
        if isinstance(value, SpecificTime) or isinstance(value, TimeInterval):
            #SpecificTime and TimeInterval have a nanos() method
            nanos = value.nanos()
        elif isinstance(value, timedelta):
            #datetime.timedelta has microseconds
            nanos = value.microseconds*1000
        else:
            #datetime.datetime has microseconds
            nanos = value.microsecond*1000
        if nanos >= self.minVal:
            return True
        else:
            return False
    def __repr__(self) -> str:
        '''
        Returns class representation
        
        :param self: Self reference
        :type self:  
        '''
        return 'MinNanosR({0})'.format(self.minVal)

class PatternR(Restriction):
    '''Requires that a string Parameter match a specified pattern
    '''
    def __init__(self, pattern:str):
        '''
        Restriction constructor
        
        :param self: Self reference
        :type self:  
        :param pattern: Regular expression pattern
        :type pattern: str
        '''
        self.pattern = pattern
        self.re = re.compile(pattern)
    def validate(self, value:str) -> bool:
        '''
        Validation function
        
        :param self: Self reference
        :type self:  
        :param value: Input value to check
        :type value: str
        '''
        if self.re.match(value):
            return True
        else:
            return False
    def __repr__(self) -> str:
        '''
        Returns class representation
        
        :param self: Self reference
        :type self:  
        '''
        return 'PatternR({0})'.format(self.pattern)

class TotalDigitsR(Restriction):
    '''Restricts the total number of digits for a float or integer Parameter.
    Not really a limit on the value but could be used to control conversions to 
    and from a string
    '''
    def __init__(self, maxVal:int):
        '''
        Restriction constructor
        
        :param self: Self reference
        :type self:  
        :param maxVal: Maximum number of digits
        :type maxVal: int
        '''
        self.maxVal = maxVal
    def validate(self, value:int | float) -> bool:
        '''
        Validation function
        
        :param self: Self reference
        :type self:  
        :param value: Input value to check
        :type value: int | float
        '''
        return True
    def __repr__(self) -> str:
        '''
        Returns class representation
        
        :param self: Self reference
        :type self:  
        '''
        return 'TotalDigitsR({0})'.format(self.maxVal)
