__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm), Brad Kizzort'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
from space import Parameter, MixedParameterValue, NullableMixedParameterValue, isSupportedParameterType, UndefinedTypeError, getParameterFunction, SpecificTime, IllegalValueError, Restriction
from typing import Any

class DemoParameter(Parameter):
    def __init__(self, name:str, type:str='str', **kwds:Any):
        self._name = name
        if isSupportedParameterType(type):
            self._type = type
        else:
            raise UndefinedTypeError('Could not create parameter of data type <{0}>'.format(type))

        self._description = ''
        self._multiplicity:NullableMixedParameterValue = None
        self._restriction:list[Restriction]   = []
        self._units  = None
        self._value:NullableMixedParameterValue = None
        self._raw   = None
        self._time  = None

        options = list(kwds.keys())
        for option in options:
            if hasattr(self, option):
                setattr(self, option, kwds[option])

    def value(self) -> NullableMixedParameterValue:
        return self._value

    def raw(self) -> NullableMixedParameterValue:
        return self._raw

    def name(self) -> str:
        return self._name
    
    def setValue(self, value: MixedParameterValue) -> None:
        # If the value supplied is not of the specified type, try to convert it using the type converter
        value = getParameterFunction(self._type)(value)
        for restriction in self._restriction:
            if not restriction.validate(value):
                raise IllegalValueError('Violates restriction {0}'.format(restriction))
        self._value = value
        self._time  = SpecificTime.now()

    def sample(self) -> dict[str, MixedParameterValue]:
        out:dict[str, MixedParameterValue] = dict()
        if self._value != None:
            out["value"] = self._value
        if self._time != None:
            out["time"] = self._time

        return out
    
    def type(self) -> str:
        return self._type
    
    def __str__(self):
        if self._value is not None:
            return str(self._value)
        else:
            return self.__repr__()

    def __repr__(self):
        r = 'Parameter({0}, dType={1}'.format(self._name, self._type)
        if self._description != '':
            r = r + ', description="{0}"'.format(self._description)
        if self._multiplicity is not None:
            r = r + ', multiplicity={0}'.format(self._multiplicity)
        if self._value is not None:
            r = r + ', _value={0}'.format(self._value)
        r = r + ')'
        return r