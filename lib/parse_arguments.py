"""
Class used to parse the arguments passed on the commandline.
Also does some basic checking.
"""
import sys
import getopt
import os
# Custom libs
import __main__ as main
from general import *
import settings

def help():
    """
    Function to display help text, invoked by passing -h or --help.
    """
print ''
print ''

# Getopt
try:
    opts, args = getopt.getopt(sys.argv[1:], "wdo:I:O:", ['dd','write','debug', 'object=', 'input=','output='])
except getopt.GetoptError as err:
    error( str(err))

for o,a in opts:
    # @TODO: Get different debugging levels working.
    #if o in ("-dd"):
    #    settings.debug = True
    #    settings.debug3 = True
    #    debug('Debugging is ON')
    #    debug3('Debugging is ON (level 3)')
    #elif o in ("-d", "--debug"):
    if o in ("-d", "--debug"):
        settings.debug = True
        debug('Debugging is ON')
    elif o in ( "-w", "--write"):
        settings.write = True
    elif o in ( "-o", "--object"):
        settings.object_name = a
    elif o in ( "-I", "--input"):
        settings.inputdir = a
    elif o in ( "-O", "--output"):
        settings.outputdir = a
    else:
        assert False

# Error checking
# Make sure that the object is defined.
if not settings.object_name in settings.objects_all and not settings.object_name == 'all':
    error("Object not known")
# Make sure that the inputdirectory exists.
if not os.path.isdir(settings.inputdir):
    error("Input directory does not exist!")
# Make sure that the outputdirectory exists.
if not os.path.isdir(settings.outputdir):
    error("Output directory does not exist!")

# Arguments cleanup.
# Add tailing / to inputdir
if not settings.inputdir.split('/').pop(-1) == '':
    settings.inputdir = settings.inputdir + '/'
# Add tailing / to outputdir
if not settings.outputdir.split('/').pop(-1) == '':
    settings.outputdir = settings.outputdir + '/'

