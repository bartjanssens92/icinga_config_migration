#!/usr/bin/python2.7
from collections import OrderedDict
# Custom
import settings
from general import *

def build_hash(object_name):
    # Build the filenames
    inputfile = settings.inputdir + object_name + 's.cfg'
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
        debug3(line)
        # Check if the line starts with a define
        if line.startswith("define"):
            config = {}
        elif line.endswith("}\n"):
            debug3(config)
            # Get the keyname
            if object_name in ['service']:
                if 'check_command' in config and isinstance(config['check_command'], list):
                    #debug("Check_command: " + str(config['check_command']))
                    #debug("Check_command: " + str(config))
                    key = str(",".join(config['check_command']))
                elif 'check_command' in config and not isinstance(config['check_command'], list):
                    #debug("Check_command: " + str(config['check_command']))
                    #debug("Check_command: " + str(config))
                    key = str(config['check_command'])
                else:
                    key = config['service_description']
                # If the key does not exist, create it
                if not key in mainhash:
                    mainhash[key] = {'hosts' : [],}
                # Fill the key with data
                mainhash[key]['hosts'].append(config['host_name'])
                mainhash[key]['config'] = config
            elif object_name in ['hostTemplate','serviceTemplate']:
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
            debug3("Linearray: " + str(linearray))
            debug3("Linearray #: " + str(len(linearray)))
            debug3("Key: " + key)
            # Check if the array contains more then one key
            if len(linearray) == 0:
                #debug('skip valueless key')
                continue
            if ',' in linearray[0]:
                value = linearray[0].split(',')
            # commands are ugly
            elif object_name in ['command','service']:
                value = str(" ".join(linearray))
            else:
                value = str(linearray[0])
            debug3('Value: ' + str(value))
            config[key] = value

    for object_t in mainhash:
        debug3('--------------------')
        debug3(object_t)
        debug3(mainhash[object_t])

    debug("Converted " + str(len(mainhash)) + " " + object_name + " objects.")
    debug("Read " + str(line_amount) + " lines.")

    return mainhash
