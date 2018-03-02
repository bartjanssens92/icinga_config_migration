#!/usr/bin/python2.7
from lib.general import *

def render():
    """Function to build the icinga hosts config file:
    const Valuename = "value"
    """
    # Default
    write_blocks = 0

    # Reading the file here as it's completely different from the other objects
    inputfile = settings.inputdir + settings.object_name + '.cfg'
    input_configfile = open(inputfile, 'r')

    # Header
    write_configfile(settings.header)

    for line in input_configfile:
        # Ignore lines starting with #
        if line.startswith('#'):
            continue
        # Skip empty lines
        elif line in ['\n', '\r']:
            continue
        # Valid lines look like: "$USER2$=public"
        linearray = line.split('=')
        key = linearray[0].replace('$','').title()
        value = linearray[1].replace('\n','')
        config_block = 'const ' + key + ' = "' + value + '"\n'

        debug("Block:\n" + config_block)

        append_configfile(config_block)
        write_blocks += 1

    input_configfile.close()
    info('Wrote ' + str(write_blocks) + ' Constant objects')

