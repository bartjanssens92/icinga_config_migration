#!/usr/bin/python2.7
from collections import OrderedDict
# Custom
import settings
from general import *

def build_hash(object_name):
    """
    Function to convert files into hashes.
    The hash's keys and values are derived per config block, definded by the keyword 'define'.
    Then the key and value are extracted on a per-line basis, assuming that there are no multilines.
    The keyname is dependend on the object type, as some objects have some edge cases.
    """
    # Build the filenames
    inputfile = settings.inputdir + object_name + 's.cfg'
    debug("Inputfile = " + inputfile)

    # Create the file objects
    input_configfile = open(inputfile, 'r')

    # Read the configfile
    mainhash = OrderedDict({})
    line_amount = 0

    # @TODO: Manage multilines
    for line in input_configfile:
        line_amount += 1
        debug4(line)
        # Check if the line starts with a define
        if line.startswith("define"):
            config = {}
        # Check if the line ends with '}'
        elif line.endswith("}\n"):
            debug4(config)
            # Get the keyname
            if object_name in ['service']:
                # For services this should be an unique name based on the check_command
                # As the check_command could have aruguments or not build the key
                if 'check_command' in config and isinstance(config['check_command'], list):
                    debug4("Check_command: " + str(config['check_command']))
                    debug4("Check_command: " + str(config))
                    key = str(",".join(config['check_command']))
                elif 'check_command' in config and not isinstance(config['check_command'], list):
                    debug4("Check_command: " + str(config['check_command']))
                    debug4("Check_command: " + str(config))
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

        # Skip empty lines
        elif line in ['\n', '\r']:
            continue
        # Ignore comments
        elif line.startswith("#"):
            continue
        # Parse the configuration block
        else:
            # Nagios config is space seperated
            linearray = line.split()
            # Nagios config the first word is the key
            # Remove the key from the array
            key = linearray.pop(0)
            debug4("Linearray: " + str(linearray))
            debug4("Linearray #: " + str(len(linearray)))
            debug4("Key: " + key)
            # Check if the array contains more then one key
            if len(linearray) == 0:
                #debug('skip valueless key')
                continue
            # Get the value, depending on what remains on the line
            if ',' in linearray[0]:
                value = linearray[0].split(',')
            # Commands and services values contain spaces, this is not wanted later on.
            elif object_name in ['command','service']:
                value = str(" ".join(linearray))
            else:
                value = str(linearray[0])

            debug4('Value: ' + str(value))
            config[key] = value

    # Debugging, print the complete object
    for object_t in mainhash:
        debug4('--------------------')
        debug4(object_t)
        debug4(mainhash[object_t])

    input_configfile.close()
    debug("Converted " + str(len(mainhash)) + " " + object_name + " objects.")
    debug("Read " + str(line_amount) + " lines.")

    return mainhash
