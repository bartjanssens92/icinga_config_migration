from lib.general import *
from lib.build_hash import build_hash

def render(object_hash):
    """
    Function to build the serviceGroup object, same as for user, host and services.
    object HostGroup "hg1" {
      assign where host.name in [ "host1", "host2" ]
    }

    object HostGroup "hg2" {
      groups = [ "hg1" ]
      assign where host.name == "host3"
    }
    """

    # Header
    write_configfile(settings.header)

    # Defaults
    write_blocks = 0

    for serviceGroup in object_hash:
        debug('--------------------')
        debug(serviceGroup)
        debug('--------------------')
        debug3(object_hash[serviceGroup])

        servicegroup_hash = object_hash[serviceGroup]

        # Init config block
        config_block = 'object HostGroup "' + servicegroup_hash['alias'] + '" {\n'
        # Hostgroup members
        if 'hostgroup_members' in servicegroup_hash:
            config_block += ' groups = [" ' + '", "'.join(servicegroup_hash['hostgroup_members']) + '" ]\n'
        # Get members
        config_block += '  assign where host.name in [ "' + '", "'.join(servicegroup_hash['members']) + '" ]\n'

        # Close the config block
        config_block += '}\n'

        # Write configblock
        debug('\n' + config_block)
        append_configfile(config_block)
        write_blocks += 1

    info('Wrote ' + str(write_blocks) + ' serviceGroups objects')
