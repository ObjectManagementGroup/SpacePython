'''
The SpecificTime and TimeInterval classes represent time within
the SpacePython procedure environment.  In this skeleton implementation,
they are a thin veneer on the Python datetime types.
'''
__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm), Brad Kizzort'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
import inspect
import datetime, time
from .errors import TimeoutError
from typing import Callable

class SpecificTime(datetime.datetime):  #Normative
    '''SpecificTime(year, month, day[, hour[, minute[, second[, microsecond]]])
    Represents a specific time for timetags and time expressions
    '''
    def dayOfYear(self) -> int:
        '''Return the day of the year with January 1 as 1.
        
        :param self: Self reference
        :type self:  
        '''
        return self.toordinal()
    def nanos(self) -> int:
        '''Return the nanoseconds
        
        :param self: Self reference
        :type self:  
        '''
        return self.microsecond*1000
    @classmethod
    def today(cls) -> 'SpecificTime':
        '''
        Returns an instance for today.
        
        :param cls: Class member
        :type cls:  '''
        t = datetime.date.today()
        return cls(t.year, t.month, t.day)
    @classmethod
    def now(cls, tz:datetime.tzinfo | None = None) -> 'SpecificTime':
        '''
        Returns an instance representing the current time.
        
        :param cls: Class member
        :type cls:  
        :param tz: Time zone
        :type tz:  '''
        t = datetime.datetime.now(tz)
        return cls(t.year, t.month, t.day, t.hour,  t.minute,\
                   t.second, t.microsecond, tz)
    @classmethod
    def fromStr(cls, strval:str) -> 'SpecificTime':
        '''Convert from a string representation to a SpecificTime
        Expected format:YYYY-MM-DDTHH:MM:SS.NNNNNN
        May optionally end with a timezone indicator, such as Z.
        
        :param cls: Class member
        :type cls:  
        :param strval: Input time string
        :type strval: str  
        '''
        t = datetime.datetime.fromisoformat(strval)
        return cls(t.year, t.month, t.day, t.hour,  t.minute,\
                   t.second, t.microsecond, t.tzinfo)
    def __str__(self) -> str:
        '''Converts a SpecificTime to the default string format
        '''
        return self.strftime('%Y-%m-%dT%H:%M:%S.%f')
    
class TimeInterval(datetime.timedelta):  #Normative
    '''TimeInterval([days[, seconds[, microseconds[, milliseconds[, minutes[, hours[, weeks]]]]]]]) 
    Represents a positive (future) or negative (elapsed) relative time interval for time expressions
    '''
    def asSeconds(self) -> float:
        '''Return entire interval as seconds
        
        :param self: Self reference
        :type self:  
        '''
        return self.total_seconds()
    def nanos(self) -> int:
        '''Return nanoseconds in the second
        
        :param self: Self reference
        :type self:          
        '''
        return self.microseconds*1000
    @classmethod
    def fromStr(cls, strval:str) -> 'TimeInterval':
        '''Convert from a string representation to a TimeInterval
        Expected format:[s]DTHH:MM:SS.NNNNNNNNN
        
        :param cls: Class reference
        :type cls:  
        :param strval: Input time string
        :type strval: str 
        '''
        isNegative = False
        days = hours = mins = secs = nsecs = 0        
        s = strval.strip()
        if s[0] == '-':  # Check for leading sign in case days are zero
            isNegative = True
            s = s[1:]
        elif s[0] == '+':
            s = s[1:]
        endOfDays = s.find('T')
        if endOfDays > 0:
            days = int(s[0:endOfDays])
            s = s[endOfDays+1:]
            if isNegative:
                days = -days
        beg = s.rfind('.')
        if beg >= 0:
            digits = len(s) - beg - 1
            digits = min(9, digits)
            nsecs = int(s[beg+1:beg+digits+1])
            nsecs = nsecs * (10**(9-digits))
            s = s[0:beg]
        beg = s.rfind(':')
        if beg >= 0:
            secs = int(s[beg+1:])
            s = s[0:beg]
        beg = s.rfind(':')
        if beg >= 0:
            mins = int(s[beg+1:])
            s = s[0:beg]
        if len(s) > 0:
            hours = int(s)
        secs = hours*3600 + mins*60 + secs
        if days == 0 and isNegative:
            dt = cls(seconds=-secs, microseconds=nsecs/1000)
        else:
            dt = cls(days, seconds=secs, microseconds=nsecs/1000)
        return dt
    def __str__(self) -> str:
        '''Converts a TimeInterval to the default string format
        
        :param self: Self reference
        :type self:  
        '''
        seconds = self.seconds
        hours   = int(seconds / 3600)
        minutes = int((seconds % 3600) / 60)
        seconds = seconds % 60
        return '{0}T{1:02d}:{2:02d}:{3:02d}.{4:06d}' \
          .format(self.days, hours, minutes, seconds,
                  self.microseconds)

def waitFor(boolean:Callable[[],bool], timeout:float=5, pollPeriod:float=0.1) -> bool:  #Normative
    '''Wait for the provided Boolean function to become true
Default timeout of 5 seconds and default polling interval of 100 milliseconds 
is used unless overridden in the call.
    
    :param boolean: Verifier function
    :type boolean: Callable[[],bool]
    :param timeout: Timeout for the verifier in seconds
    :type timeout: float 
    :param pollPeriod: Frequency of polling in seconds
    :type pollPeriod: float 
    '''
    frame = inspect.stack()[1]
    line = frame[0].f_lineno
    del frame
    while boolean() is not True:
        if timeout <= 0.0:
            raise TimeoutError('Wait at line %d timed out' % line)
        else:
            time.sleep(pollPeriod)
            timeout -= pollPeriod
    return True

def wait(seconds:float) -> None:  #Normative
    '''Wait for the specified number of seconds 
    
    :param seconds: Number of seconds to wait
    :type seconds: float 
    '''
    time.sleep(seconds)

def waitUntil(specificTime:datetime.datetime) -> None:  #Normative
    '''Wait for a SpecificTime - returns immediately if time is in the past
    
    :param specificTime: Time reference to wait until
    :type specificTime: SpecificTime
    '''
    # use same timezone for now as the provided datetime
    now = SpecificTime.now(specificTime.tzinfo)
    delta = (specificTime - now).total_seconds()
    if delta > 0:
        time.sleep(delta)

