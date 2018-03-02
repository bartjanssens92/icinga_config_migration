#!/usr/bin/python2.7
from collections import OrderedDict
# Custom
from lib.general import *
from notifications import render_notifications

def render(object_hash, commands_hash, servicetemplates_hash, contact_hash):
    """Function to build the icinga services config file:
    apply Service "service1" {
      import "generic-service"
      check_command = "test_check"

      assign where host.name in [ "localhost1", "localhost2" ]
      vars.argument = "test"
    }
    """
    # Header
    write_configfile(settings.header)

    # Defaults
    write_blocks = 0

    for service in object_hash:
        debug('--------------------')
        debug(service)
        debug('--------------------')
        debug3(object_hash[service]['config'])

        # Make sure the servicename is sane
        if '!' in service:
            service_name = service.split('!')[0]
        else:
            service_name = service

        # Service name needs to be uniq
        sane_service = service.replace('!','_').replace('/','').replace('"','')

        # Build the config_block
        config_block = 'apply Service "' + sane_service + '" {\n'
        debug(sane_service)

        # Get the import
        # Every service needs the import statement otherwise use the default one
        if 'use' in object_hash[service]['config']:
            config_block += '  import "' + object_hash[service]['config']['use'] + '"\n'
        else:
            config_block += '  import "' + settings.default_service_import + '"\n'

        # Get the check_command
        if 'check_command' in object_hash[service]['config']:
            check_command = object_hash[service]['config']['check_command']

            # If it's a list, join it
            if isinstance(check_command, list):
                check_command = ",".join(check_command)

            debug("Check command: " + check_command)

            # This means that the command is passing options
            if '!' in service:
                sane_check_command = check_command.split('!')[0]
                config_block += '  check_command = "' + sane_check_command + '"\n'
                config_block += '\n'

                # Get the arguments of the command
                arguments = commands_hash[sane_check_command]
                debug('Arguments: ' + str(arguments))

                # Build the values to pass
                argument_i = 1
                for key in arguments:
                    # Check if the value of the key is $ARG\n$
                    if arguments[key] in ['$ARG1$','$ARG2$','$ARG3$','$ARG4$']:
                        # Use the unique command name
                        key = 'vars.' + service_name.replace('-','_') + '_' + key.translate(None, '-')
                        value = check_command.split('!')[argument_i].replace('"','\\"')
                        config_block += '  ' + key + ' = "' + value + '"\n'
                        argument_i+= 1
                    else:
                        debug('Could not build var name for: ' + key)
                        pass

            else:
                config_block += '  check_command = "' + check_command + '"\n'

        # If there is no check_command try and figure out what check_command to use
        # Get is from the templates that are included
        else:
            # Figure out the check_command
            check_command = find_check_command(servicetemplates_hash, object_hash[service]['config']['use'])
            debug('Figured out check command: ' + str(check_command))
            # Catch errors, but don't stop on them
            if check_command == 'error':
                config_block += '  check_command = "Unable to find check_command"\n'
            else:
                config_block += '  check_command = "' + check_command + '"\n'

        # Notifications
        config_block += '\n'
        config_block += render_notifications(object_hash[service]['config'],contact_hash,'service')

        # Get the hosts
        config_block += '  assign where host.name in [ "' + '", "'.join(object_hash[service]['hosts']) + '" ]\n'

        # Close the config_block
        config_block += '}\n'

        # Print the config in the config file
        debug("\n" + config_block)
        append_configfile(config_block)
        write_blocks += 1

    info('Wrote ' + str(write_blocks) + ' service objects')

def find_check_command(template_hash, service):
    """
    Function to find what service uses what check_command for apply service configuration.
    Recusive function as sometimes a template just include another one.
    """
    if 'check_command' in template_hash[service]:
        return template_hash[service]['check_command']
    elif 'import' in template_hash[service]:
        return find_check_command(template_hash, template_hash[service]['import'])
    else:
        return 'error'
