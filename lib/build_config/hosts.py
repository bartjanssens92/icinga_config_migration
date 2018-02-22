#!/usr/bin/python2.7
import lib.settings
from lib.general import *
from notifications import render_notifications

def render(object_hash, contact_hash):
    """Function to build the icinga hosts config file:
    object Host "$hostname" {
      import "linux-host"

      address = "$address"

      vars.environment = "$environment"

      vars.notification["$notification_method"] = {
        groups = [ "$contactgroups" ]
        users = [ "$contacts" ]
      }
    }
    """
    # Default
    default_use = 'development-host'
    default_host_type = 'linux-host'
    write_blocks = 0

    # Header
    write_configfile(settings.header)

    # Environment array
    env_array = ['development-host','production-host','critical-host']

    # Loop over the hosts
    for host in object_hash:

        # Debug
        debug('--------------------')
        debug("host_hash: " + str(object_hash[host]))

        host_hash = object_hash[host]

        # Build the head
        config_block = 'object Host "' + host + '" {\n'

        # Get the environment from the host_hash['use']
        if not 'use' in host_hash:
            host_type = default_host_type
            config_block += '  import "' + default_use + '"\n'
        # Check if the use is a list or not
        elif isinstance(host_hash['use'], list):
            # Loop over all the use classes
            for use in host_hash['use']:
                config_block += '  import "' + use + '"\n'
        else:
            config_block += '  import "' + str(host_hash['use']) + '"\n'

        # Build the basic config
        config_block += '\n'
        config_block += '  address = "' + host_hash['address'] + '"\n\n'

        # Check the notifications
        config_block += render_notifications(host_hash, contact_hash)

        # Close the host config block
        config_block += '}\n'

        debug(config_block)
        append_configfile(config_block)
        write_blocks += 1

    info('Wrote ' + str(write_blocks) + ' host objects')

