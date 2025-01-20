'''Shell command line parsing of SOLM Parameters
'''
__author__    = 'Space Domain Task Force (https://www.omg.org/solm/index.htm), Brad Kizzort'
__copyright__ = 'Object Management Group under RF-Limited license (https://www.omg.org/cgi-bin/doc.cgi?ipr)'
#
import sys
class Namespace(object):
    '''A Namespace object stores attributes for parsed input.
    '''
    pass
#
def parseArgs(progname, description='', parameters=[], args=None):
    '''Parse the input arguments according to the parameter list
    uses sys.argv[1:] if no arguments are supplied.  Returns a
    Namespace object with attributes named after the supplied list
    of parameters.
    '''
    if args is None:
        args = sys.argv[1:]
    parser = Parser(progname, description, parameters)
    return parser.parse(args)
#
class Parser(object):
    '''Internal class for command line parse
    '''
    def __init__(self, progname, description, parameters):
        self.progname   = progname
        self.description= description
        self.result     = Namespace()
        self.parameters = parameters
        self.parms      = dict()
        for parm in parameters:
            self.result.__setattr__(parm.name, parm.value_)
            self.parms[parm.name] = parm
    def parse(self, args):
        positional = True   # Assume the parameters are positional
        index      = 0
        for arg in args:
            if positional and index >= len(self.parms):
                self.error('extra argument %s' % arg)
            if arg.startswith('--'):
                positional = False
                equals = arg.find('=')
                if equals < 0:
                    if arg == '--help':
                        self.print_usage()
                        sys.exit(0)
                    else:
                        argname = arg
                        value   = ''
                else:
                    argname = arg[0:equals]
                    value   = arg[equals+1:]
                name = argname[2:]
                if name in self.parms:
                    self.parseValue(self.parms[name], value)
                else:
                    self.error('unrecognized argument %s' % argname)
            elif positional:
                self.parseValue(self.parameters[index], arg)
                index += 1
            else:
                self.error('cannot use positional after keyword argument')
        self.checkComplete()
        return self.result
    def parseValue(self, parm, value):
        #save old value so we don't change callers parameters
        oldval = parm.value_
        try:
            parm.setValue(value)
        except Exception as e:
            self.error('{0} for {1}'.format(e, parm.name))
        setattr(self.result, parm.name, parm.value_)
        parm.value_ = oldval
    def checkComplete(self):
        for parm in self.parameters:
            if getattr(self.result, parm.name) is None:
                self.error('missing parameter %s' % parm.name)
    def usage(self):
        guide = self.progname
        for parm in self.parameters:
            guide += ' --%s=<%s>' % (parm.name, parm.dType)
        guide += '\n'
        return guide
    def error(self, message):
        sys.stderr.write(message)
        sys.stderr.write('\n')
        self.print_usage()
        sys.exit(2)
    def print_usage(self):
        sys.stderr.write(self.usage())
        sys.stderr.write(self.description)

        
