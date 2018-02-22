import sys
import getopt
import os
# Custom libs
from general import *
import settings

# Getopt
try:
    opts, args = getopt.getopt(sys.argv[1:], "wdo:I:O:", ['dd','write','debug', 'object=', 'input=','output='])
except getopt.GetoptError as err:
    error( str(err))
for o,a in opts:
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
if not settings.object_name in settings.objects_all and not settings.object_name == 'all':
    error("Object not known")
if not os.path.isdir(settings.inputdir):
    error("Input directory does not exist!")
if not os.path.isdir(settings.outputdir):
    error("Output directory does not exist!")
if not settings.inputdir.split('/').pop(-1) == '':
    # Add tailing / to the inputdir
    settings.inputdir = settings.inputdir + '/'
if not settings.outputdir.split('/').pop(-1) == '':
    # Add tailing / to the outputdir
    settings.outputdir = settings.outputdir + '/'

