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

# Defaults
scriptname = main.__file__
helptext = 'Usage: ' + scriptname + ' [OPTIONS]\n\n'
options = "hwdo:I:O:"
options_long = ['help', 'write', 'debug', 'object=', 'input=', 'output=']
options_desc = [
        'Show help',
        '(Depricated) Write the configfiles',
        'Enable debugging ( level 1 )',
        'Generate only the configuration of this object',
        'Use this directoy as input',
        'Which directory to write the configfiles in',
        ]

# Generate the help text
i = 0
# Include all the options
for option in list(options):
    # Ignore ':'
    if not option == ':':
        helptext += '  -' + option + ', --' + options_long[i] + '\t\t' + options_desc[i] + '\n'
        i += 1
    else:
        pass

helptext += '\nExamples:\n\n'
helptext +='* Generate configuration for all the objects:\n  ' + scriptname + '\n'
helptext +='* Generate configuration for the host object:\n  ' + scriptname + ' -o host\n'
helptext +='* Generate configuration from /tmp/in:\n  ' + scriptname + ' -I /tmp/in\n'

# Getopt
try:
    opts, args = getopt.getopt(sys.argv[1:], options, options_long )
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
    elif o in ( "-h", "--help"):
        print helptext
        sys.exit(0)
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

