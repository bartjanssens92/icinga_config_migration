#!/usr/bin/python2.7
from general import error,debug,info
from collections import OrderedDict

def build_hash(object_name,inputdir):
    """This function returns the object hash"""

    # Build the filenames
    inputfile = inputdir + object_name + 's.cfg'
    debug("Inputfile = " + inputfile)

    # Create the file objects
    input_configfile = open(inputfile, 'r')

    # Get the keyname
    #if object_name in ['service']:
    #    keyname = '_SERVICE_ID'
    #else:
    #    keyname = object_name + '_name'

    # Read the configfile
    mainhash = OrderedDict({})
    line_amount = 0
    for line in input_configfile:
        line_amount += 1
        #debug(line)
        # Check if the line starts with a define
        if line.startswith("define"):
            config = {}
        elif line.endswith("}\n"):
            #debug(config)
            # Get the keyname
            if object_name in ['service']:
                if not config['service_description'] in mainhash:
                    mainhash[config['service_description']] = {'hosts' : {},}
                mainhash[config['service_description']]['hosts'][config['host_name']] = config
            elif object_name in ['hostTemplate']:
                mainhash[config['name']] = config
            else:
                mainhash[config[object_name + '_name']] = config
            #mainhash[config[keyname]] = config
        elif line in ['\n', '\r']:
            # Skip emtpy lines
            continue
        elif line.startswith("#"):
            # Ignore comments
            continue
        else:
            linearray = line.split()
            key = linearray.pop(0)
            #debug(key)
            if ',' in linearray[0]:
                value = linearray[0].split(',')
            # commands are ugly
            elif object_name in ['command']:
                value = str(" ".join(linearray))
            else:
                value = str(linearray[0])
            config[key] = value

    #for object_t in mainhash:
    #    debug('--------------------')
    #    debug(object_t)
    #    debug(mainhash[object_t])

    info("Converted " + str(len(mainhash)) + " " + object_name + " objects.")
    info("Read " + str(line_amount) + " lines.")
    return mainhash
