#!/usr/bin/env python

import argparse
import os
import sys
import time

# Since posix symlinks are not supported on windows, let's
# explicitly update sys.path.
try:
    import mepreader as mr
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
    import mepreader as mr

#---------------------------------------------------------------------------
class MEPReaderParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

#---------------------------------------------------------------------------
if __name__ == '__main__':

    parser = MEPReaderParser()

    parser.add_argument("--version", action="version",
        version="%(prog)s {}".format(mr.__version__))

    parser.add_argument("-v", "--verbose", dest="verbose_count",
        action="count", default=0,
        help="increases log verbosity for each occurence.")

    parser.add_argument('--plot',
        dest='plotSignal', action='store_true', default=False,
        help='Plot the signal. Requires matplotlib. (Helps to debug missed triggers)')

    parser.add_argument('--plotDerivative',
    	dest='plotDerivative', action='store_true', default=False,
    	help='Plot the derivative under the EMG signal.  (Helps to debug missed triggers)')

    parser.add_argument("-i", "--inputFile", dest="filename",
    	required=True, type=argparse.FileType('r'))

    parser.add_argument('-o', #metavar="output",
        type=argparse.FileType('w'), default=sys.stdout,
        dest='output_file',
        help="redirect output to a file")

    arguments = parser.parse_args(sys.argv[1:])

    if arguments.verbose_count == 0:
        arguments.verbose_count = mr.VERBOSE

    mr.ReadAnalogData(inputFile=arguments.filename,
    	              verbose=arguments.verbose_count,
    	              outputPath=arguments.output_file,
    	              plotDerivative=arguments.plotDerivative,
    	              plotSignal=arguments.plotSignal)