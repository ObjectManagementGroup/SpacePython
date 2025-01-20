'''
operatorQuery prompts the operator for inputs.
'''
__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm), Brad Kizzort'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
# The simplicity of this query implementation does not support 
# a <Cancel> or <Abort> input from the operator, but it is 
# anticipated that a GUI-based query could, so exceptions are 
# defined for the interface.
from .errors import QueryAbortedError, QueryCanceledError
from .shell import Namespace
#
# This provides a simple console input implementation of the operator 
# query.  It is expected that an integrated procedure environment 
# would provide GUI dialog instead.
#
def operatorQuery(prompt='', **parameters):  #Normative
    '''Accepts an optional prompt string and keyword=value pairs.
    If there are no keyword=value pairs, no values will be requested 
    from the operator.  A default value may be supplied for the keyword
    otherwise a value of '' should be used. 
    If no keyword=value pairs are specified and the prompt string is empty, 
    the operator will be asked to continue before returning.
    Returns an space.shell.Namespace object with values provided by the operator
    '''
    namespace = Namespace()
    if len(parameters) > 0:
        if prompt != '':
            print(prompt, '\n')
        for name in list(parameters.keys()):
            pr_str = 'New value for %s, or <Enter> for default (%s) ' % (name,parameters[name])
            response = input(pr_str)
            if response != '':
                namespace.__setattr__(name, response)
            else:
                namespace.__setattr__(name, parameters[name])
    else: # No values to get
        if prompt != '':
            response = input(prompt)
        else:
            response = input('<Enter> to continue')
    return namespace
