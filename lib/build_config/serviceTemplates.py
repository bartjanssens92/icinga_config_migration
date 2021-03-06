#!/usr/bin/python2.7
from collections import OrderedDict
# Custom
from lib.general import *
from lib.build_hash import build_hash
from notifications import render_notifications
from commands import get_hash as get_commands_hash

def get_hash():
    """
    Function to return the rendered hash.
    Usefull when other object need values from this one.
    """
    return render(build_hash('serviceTemplate'), get_commands_hash(), build_hash('contact'), False)

def render(object_hash, commands_hash, contact_hash, write_config=True):
    """Function to build the icinga services templates file:
    template Service "generic-service" {
      max_check_attempts = 3
      check_interval = 1m
      retry_interval = 30s
    }
    """
    # Header
    if write_config:
        write_configfile(settings.header)

    #Defaults
    write_blocks = 0
    service_template_hash = OrderedDict({})

    for service in object_hash:
        debug('--------------------')
        debug(service)
        debug('--------------------')
        debug3(object_hash[service])

        # Define config_block
        config_block = 'template Service "' + object_hash[service]['name'] + '" {\n'
        template_hash = {}

        # Check for common params
        if 'use' in object_hash[service] and 'check_command' in object_hash[service]:
            config_block += '  import "' + object_hash[service]['use'] + '"\n'
            template_hash['import'] = object_hash[service]['use']
        elif 'use' in object_hash[service]:
            config_block += '  import "' + object_hash[service]['use'] + '"\n'
            template_hash['import'] = object_hash[service]['use']
        elif 'check_command' in object_hash[service]:
            config_block += '  import "' + settings.default_service_import + '"\n'
        else:
            pass

        if 'max_check_attempts' in object_hash[service]:
            config_block += '\n'
            config_block += '  max_check_attempts = ' + object_hash[service]['max_check_attempts'] + '\n'
        if 'check_interval' in object_hash[service]:
            config_block += '  check_interval = ' + object_hash[service]['check_interval'] + 'm\n'
        if 'retry_interval' in object_hash[service]:
            config_block += '  retry_interval = ' + object_hash[service]['retry_interval'] + 's\n'


        # Check if there is a check_command defined
        if 'check_command' in object_hash[service]:

            # Spacer
            config_block += '\n'

            # Setup the check_command
            check_command = object_hash[service]['check_command']

            # Check if it's a list
            if isinstance(check_command,list):
                check_command = ','.join(check_command)

            # Check if it passes args
            if '!' in check_command:
                check_command_list = check_command.split('!')

                # Get the check_command
                check_command = check_command_list.pop(0)
                debug("Check_command: " + check_command)
                config_block += '  check_command = "' + check_command + '"\n'

                # Add to the template
                template_hash['check_command'] = check_command

                # Get the arguments of the command
                arguments = commands_hash[check_command]
                debug('Arguments: ' + str(arguments))

                # Build the values to pass
                argument_i = 0
                for key in arguments:
                    # Check if the value of the key is $ARG\n$
                    if arguments[key] in ['$ARG1$','$ARG2$','$ARG3$','$ARG4$']:
                        # Use the unique variable name
                        key = 'vars.' + check_command.replace('-','_') + '_' + key.translate(None, '-')
                        value = check_command_list[argument_i]
                        config_block += '  ' + key + ' = "' + value + '"\n'
                        argument_i+= 1
                    else:
                        pass

            # No arguments in for the check_command
            else:
                config_block += '  check_command = "' + object_hash[service]['check_command'] + '"\n'

                # Add to the template
                template_hash['check_command'] = object_hash[service]['check_command']

            # Notification stuff
            config_block += '\n'
            config_block += render_notifications(object_hash[service], contact_hash, 'service')

        # Close the config block
        config_block += '}\n'
        debug('complete config block:\n' + config_block)

        if write_config:
            # Write the config file
            append_configfile(config_block)
            write_blocks += 1
        else:
            service_template_hash[object_hash[service]['name']] = template_hash

    if write_config:
        info('Wrote ' + str(write_blocks) + ' serviceTemplate objects')
    else:
        # Return the hash
        return service_template_hash

