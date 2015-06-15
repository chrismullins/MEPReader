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

    def is_valid_file(parser, arg):
	    if not os.path.exists(arg):
	        parser.error("The file %s does not exist!" % arg)
	    else:
	        return open(arg, 'r')  # return an open file handle

    def extant_file(x):
	    """
	    'Type' for argparse - checks that file exists but does not open.
	    """
	    if not os.path.exists(x):
	        raise argparse.ArgumentError("{0} does not exist".format(x))
	    return x

#---------------------------------------------------------------------------
if __name__ == '__main__':

    parser = MEPReaderParser()

    parser.add_argument("--version", action="version",
        version="%(prog)s {}".format(mr.__version__))

    parser.add_argument("-v", "--verbose", dest="verbose_count",
        action="count", default=0,
        help="increases log verbosity for each occurence.")

    # parser.add_argument("--inputFile", dest="filename", required=True,
    #                 help="input data file from spike2", metavar="FILE",
    #                 type=lambda x: parser.is_valid_file(parser, x))
    # parser.add_argument("-i", "--inputFile",
    #     dest="filename", required=True, type=parser.extant_file,
    #     help="input file with two matrices", metavar="FILE")
    parser.add_argument("-i", "--inputFile", dest="filename", required=True, type=argparse.FileType('r'))

    arguments = parser.parse_args(sys.argv[1:])

    if arguments.verbose_count == 0:
        arguments.verbose_count = mr.VERBOSE

    mr.ReadAnalogData(inputFile=arguments.filename,
    	              verbose=arguments.verbose_count)