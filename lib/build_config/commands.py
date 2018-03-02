#!/usr/bin/python2.7
from collections import OrderedDict
# Custom
from lib.general import *
from lib.build_hash import build_hash
from convert import convert_macro

def get_hash():
    """
    Function to return the rendered hash.
    Usefull when other objects need values from this one.
    """
    return render(build_hash('command'),False)

def render(object_hash,write_config=True):
    """Function to build the commands
    They should look like this example:
    object CheckCommand "my-ping-check" {
      command = [
        PluginDir + "/check_ping", "-4"
      ]

      arguments = {
        "-H" = "$ping_address$"
        "-w" = "$ping_wrta$,$ping_wpl$%"
        "-c" = "$ping_crta$,$ping_cpl$%"
        "-p" = "$ping_packets$"
        "-t" = "$ping_timeout$"
      }

      vars.ping_address = "$address$"
      vars.ping_wrta = 100
      vars.ping_wpl = 5
      vars.ping_crta = 200
      vars.ping_cpl = 15
    }

    object Service "my-ping" {
      import "generic-service"
      host_name = "my-server"
      check_command = "my-ping-check"

      vars.ping_wrta = 100
      vars.ping_wpl = 20
      vars.ping_crta = 500
      vars.ping_cpl = 60
    }
    """
    # Header
    if write_config:
        write_configfile(settings.header)
    else:
        return_hash = OrderedDict({})

    # Defaults
    snmp = False
    write_blocks = 0

    for command in object_hash:
        debug('--------------------')
        debug(command)
        debug('--------------------')
        debug3(object_hash[command])
        # Ignore notifications as those are dealth with somewhere else
        # The are also included in the default icinga configuration
        if 'notify' in command:
            debug('notify found, skipping')
            continue
        # SNMP is a little snowflake we need to handle with care
        if 'snmp' in command:
            debug('SNMP found, take care of the -o option')
            snmp = True

        command_array = object_hash[command]['command_line'].split(' ')

        # Loop in the command
        prev_key = False
        multi_value = False
        arguments = OrderedDict({})
        ignore_dash = False

        # Build the arguments hash
        """
        This converts this
        {'command_line': '$USER1$/check_traffic.sh -V 1 -C public -H $HOSTADDRESS$ -N $ARG1$ -w 90000,90000 -c 95000,95000 -K -B', 'command_name': 'check_centreon_traffic_32bit'}
        into this:
        {'-C': 'public', '-c': '95000,95000', '-N': '$ARG1$', '-H': '$HOSTADDRESS$', '-K': False, '-w': '90000,90000', '-V': '1'}
        """
        for argument in command_array:
            # Get the key first
            debug('ARG: ' + str(argument))
            # To catch smth like '-B -K'
            if prev_key and not key in arguments:
                arguments[key] = ''
                debug('Created new key: ' + key)
            # If the previous was a key and it's the last element
            # To catch stuff that ends with -B and the key not having a value
            if prev_key and argument == command_array[-1] and not '=' in argument and argument.startswith('-'):
                arguments[argument] = ''
                debug('Last element')
                debug('Created new key: ' + argument)
            # Assume a key is always starting with a '-' unless we are ignoring it
            if argument.startswith('-') and not ignore_dash:
                # -h=
                # --host=
                if '=' in argument:
                    key = argument.split('=').pop(0)
                    # Check if it's smth like '--expect="HTTP/1.1 200 OK'
                    if argument.split('=').pop().startswith("'") and argument.split('=').pop().endswith("'"):
                        arguments[key] = argument.split('=').pop()
                    # Same but within '"'
                    elif argument.split('=').pop().startswith('"') and argument.split('=').pop().endswith('"'):
                        arguments[key] = argument.split('=').pop()
                    # As we are splitting on ' ' this means that quoted values ( -b 'some values with spaces' ) are broken up
                    # This accounts for that by setting the multivalue parameter, used later on
                    elif argument.split('=').pop().startswith('"'):
                        multi_value = True
                        debug('new multivalue found, starting with "')
                        arguments[key] = quoting_sane(argument.split('=').pop())
                    # Same for stuff quoted with '
                    elif argument.split('=').pop().startswith("'"):
                        multi_value = True
                        debug('new multivalue found, starting with \'')
                        arguments[key] = quoting_sane(argument.split('=').pop())
                    # Nothing special, just add it
                    else:
                        arguments[key] = argument.split('=').pop()
                # -H
                # --host
                else:
                    # Only add the argument key, expect the next one to be a value
                    prev_key = True
                    key = argument
            # If it's a value
            # 20
            # $HOSTADDRESS$
            # Ignore the command: '$USER1$/check_snmp_printer'
            elif argument.startswith('$') and not argument.endswith('$') and '/' in argument:
                debug('command found, ignoring')
                continue
            # See if a shell get's called: '/bin/sh'
            elif argument.startswith('/'):
                debug('command found, ignoring')
                continue
            # Check if the argument is quoted
            elif argument.startswith("'") and argument.endswith("'"):
                debug('starting and ending with \'')
                prev_key = False
                arguments[key] = argument
            # Same but for " quotes
            elif argument.startswith('"') and argument.endswith('"'):
                debug('starting and ending with \"')
                prev_key = False
                arguments[key] = argument
            # To catch smth like '"HTTP/1.1 200 OK"'
            elif argument.startswith('"') and not multi_value:
                multi_value = True
                prev_key = False
                ignore_dash = True
                arguments[key] += ' ' + quoting_sane(argument)
            # To catch smth like '"HTTP/1.1 200 OK"'
            elif argument.endswith('"') and multi_value:
                multi_value = False
                prev_key = False
                ignore_dash = False
                debug('end multivalue, ending with "')
                arguments[key] += ' ' + quoting_sane(argument)
            # To catch smth like "'HTTP/1.1 200 OK'"
            elif argument.startswith("'") and not multi_value:
                multi_value = True
                prev_key = False
                ignore_dash = True
                debug('new multivalue found, starting with \'')
                arguments[key] += ' ' + quoting_sane(argument)
            # To catch smth like "'HTTP/1.1 200 OK'"
            elif argument.endswith("'") and multi_value:
                multi_value = False
                prev_key = False
                ignore_dash = False
                debug('end multivalue, ending with \'')
                arguments[key] += ' ' + quoting_sane(argument)
            # To catch smth like '--expect="HTTP/1.1 200 OK"
            elif multi_value:
                prev_key = False
                debug('next multivalue: ' + argument)
                arguments[key] += ' ' + quoting_sane(argument)
            # Only add the argument if the pervious thing added was a key
            # To ensure that nothing gets overwritten
            elif prev_key:
                arguments[key] = argument
            # If it gets here we are missing a case
            else:
                prev_key = False
                debug('no clue what to do with this!')

        # Start the arguments block
	arguments_block = '  arguments = {\n'
        vars_block = '\n'
        command_options = ''

        # Build the keys block
        debug('Command arguments: ' + str(arguments))

        for key in arguments:
            # Build the arguments block
            # If the value block is empty, do not add a parameter for it
            if not arguments[key]:
                command_options += " " + key
                debug('Command options: ' + str(command_options))
            # For snmp's -o option
            # SNMP does some interpolation: '-o .1.3.6.1.4.1.13742.6.5.2.4.1.4.1.1.$ARG1$.6'
            elif key == '-o' and 'ARG1' in arguments[key] and arguments[key].startswith('.'):
                arguments_block += '    "' + key + '"'
                arguments_block += '  = "' + arguments[key].replace('ARG1', command + '_' + key.replace('-','')) + '"\n'
            else:
                arguments_block += '    "' + key + '"'
                arguments_block += ' = "$' + command.replace('-','_') + '_' + key.translate(None, '-') + '$"\n'

            # Build the vars block
            debug('' + str(arguments[key]))

            if not arguments[key]:
                # No value to add if there is none
                continue
            elif key == '-o' and 'ARG1' in arguments[key] and arguments[key].startswith('.'):
                value = ' = ""'
            # Get host parameters setup
            elif arguments[key].startswith('$_') and arguments[key].endswith('$'):
                value = ' = "' + parse_variable(arguments[key]) + '"'
            elif arguments[key].startswith("'$_") and arguments[key].endswith("$'"):
                value = ' = "' + parse_variable(arguments[key]) + '"'
            # Get the $HOSTNAME$ type parameters to the new format
            elif arguments[key].startswith('$') and arguments[key].endswith('$'):
                value = ' = "' + convert_macro(arguments[key]) + '"'
            # The value needs to be quoted with "
            # If it already is, just add it
            elif arguments[key].startswith('"') and arguments[key].endswith('"'):
                value = ' = ' + arguments[key]
            # Otherwise if it's using ', replace those
            elif arguments[key].startswith("'") and arguments[key].endswith("'"):
                value = '= "' + str(arguments[key].translate(None, "'")) + '"'
            # Numbers don't have to be quoted
            elif is_number(arguments[key]):
                value = ' = ' + arguments[key]
            # Nothing special, just add it
            else:
                value = ' = "' + str(arguments[key]) + '"'

            # To make sure to have unique variable names, use the command and replace the illigal characters
            vars_block += '  vars.' + command.replace('-','_') + '_' + key.translate(None, '-') + value + '\n'

        # Close the arguments block
	arguments_block = arguments_block + '  }\n'

	# Build the configblock
	config_block = 'object CheckCommand "' + command + '" {\n'
	config_block += '  command = [\n'
        # Catch the /bin/sh -c and stuff
        if command_array[0].startswith('/'):
	    config_block += '    "' + command_array[0] + '"\n'
        # @TODO: Check where the command is housed on the system
        elif command_options:
	    config_block += '    PluginDir + "/' + command_array[0].split('/').pop() + '", "' + command_options.lstrip(' ') + '"\n'
        else:
	    config_block += '    PluginDir + "/' + command_array[0].split('/').pop() + '"\n'

        # Close the config block
	config_block = config_block + '  ]\n\n'

        # Add the arguments and the vars blocks and close the command block
        config_block = config_block + arguments_block + vars_block + '}\n'
        debug(config_block)

        # Write the config block
        if write_config:
            append_configfile(config_block)
            write_blocks += 1
        # Or append to the return_hash
        else:
            return_hash[command] = arguments

    if write_config:
        info('Wrote ' + str(write_blocks) + ' command objects')
    else:
        return return_hash

def parse_variable(name):
    """
    Function to convert a variable name into a $host.paramname$ or $service.paramname.
    """
    if 'HOST' in name:
        return '$host.' + name.replace('HOST','').replace('$','').replace('"','').replace("'",'').replace('_','',1).lower() + '$'
    elif 'SERVICE' in name:
        return '$service.' + name.replace('SERVICE','').replace('$','').replace('"','').replace("'",'').replace('_','',1).lower() + '$'
    else:
      return 'Error'

def quoting_sane(i):
    """
    Function to convert the quoting.
    Includes if statements for all the cases but only one is used.
    """
    if '""' in i:
        debug('found ""')
        pass
    if '"' in i:
        debug('found "')
	return i.replace('"','')
        debug('found ""')
    if "''" in i:
        debug("found ''")
        pass
    if "'" in i:
        debug("found '")
        pass
    return i

