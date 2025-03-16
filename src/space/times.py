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

class SpecificTime(datetime.datetime):  #Normative
    '''SpecificTime(year, month, day[, hour[, minute[, second[, microsecond]]])
    Represents a specific time for timetags and time expressions
    '''
    def dayOfYear(self):
        '''Return the day of the year with January 1 as 1.
        '''
        begin = datetime.datetime(self.year, 1, 1)
        diff  = self - begin
        return (diff.days + 1)
    def nanos(self):
        '''Return the nanoseconds
        '''
        return self.microseconds*1000
    @classmethod
    def today(cls):
        t = datetime.date.today()
        return cls(t.year, t.month, t.day)
    @classmethod
    def now(cls):
        t = datetime.datetime.now()
        return cls(t.year, t.month, t.day, t.hour,  t.minute,\
                   t.second, t.microsecond)
    @classmethod
    def fromStr(cls, strval):  
        '''Convert from a string representation to a SpecificTime
        Expected format:YYYY-MM-DDTHH:MM:SS.NNNNNN
        '''
        strval = strval.strip()
        if len(strval) <= 10:
            t = datetime.datetime.strptime(strval, '%Y-%m-%d')
        elif len(strval) <= 16:
            t = datetime.datetime.strptime(strval, '%Y-%m-%dT%H:%M')
        else:
            t = datetime.datetime.strptime(strval, '%Y-%m-%dT%H:%M:%S.%f')
        return cls(t.year, t.month, t.day, t.hour,  t.minute,\
                   t.second, t.microsecond)
    def __str__(self):
        '''Converts a SpecificTime to the default string format
        '''
        return self.strftime('%Y-%m-%dT%H:%M:%S.%f')
    
class TimeInterval(datetime.timedelta):  #Normative
    '''TimeInterval([days[, seconds[, microseconds[, milliseconds[, minutes[, hours[, weeks]]]]]]]) 
    Represents a positive (future) or negative (elapsed) relative time interval for time expressions
    '''
    def asSeconds(self):
        ''' Return entire interval as seconds
        '''
        return self.total_seconds()
    def nanos(self):
        ''' Return nanoseconds in the second
        '''
        return self.microseconds*1000
    @classmethod
    def fromStr(cls, strval):  
        '''Convert from a string representation to a TimeInterval
        Expected format:[s]DTHH:MM:SS.NNNNNNNNN
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
    def __str__(self):
        '''Converts a TimeInterval to the default string format
        '''
        seconds = self.seconds
        hours   = seconds / 3600
        minutes = (seconds % 3600) / 60
        seconds = seconds % 60
        return '{0}T{1:02d}:{2:02d}:{3:02d}.{4:06d}' \
          .format(self.days, hours, minutes, seconds,
                  self.microseconds)

def waitFor(boolean, timeout=5, pollPeriod=0.1):  #Normative
    '''Wait for the provided Boolean function to become true
Default timeout of 5 seconds and default polling interval of 100 milliseconds 
is used unless overridden in the call.
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

def wait(seconds):  #Normative
    '''Wait for the specified number of seconds 
    '''
    time.sleep(seconds)

def waitUntil(specificTime):  #Normative
    '''Wait for a SpecificTime - returns immediately if time is in the past
    '''
    now = SpecificTime.now()
    delta = (specificTime - now).total_seconds()
    if delta > 0:
        time.sleep(delta)

