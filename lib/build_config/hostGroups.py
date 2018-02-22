from lib.general import *
from lib.build_hash import build_hash

def render(object_hash):
    """
    Function to build the hostGroup object, same as for user, host and hosts.
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

    for hostGroup in object_hash:
        debug('--------------------')
        debug(hostGroup)
        debug('--------------------')
        debug3(object_hash[hostGroup])

        hostgroup_hash = object_hash[hostGroup]

        # Init config block
        config_block = 'object HostGroup "' + hostgroup_hash['alias'] + '" {\n'
        # Hostgroup members
        if 'hostgroup_members' in hostgroup_hash and len(hostgroup_hash['hostgroup_members']) > 1:
            config_block += ' groups = [" ' + '", "'.join(hostgroup_hash['hostgroup_members']) + '" ]\n'
        elif 'hostgroup_members' in hostgroup_hash:
            config_block += ' groups = [" ' + hostgroup_hash['hostgroup_members'] + '" ]\n'
        # Get members
        config_block += '  assign where host.name in [ "' + '", "'.join(hostgroup_hash['members']) + '" ]\n'

        # Close the config block
        config_block += '}\n'

        # Write configblock
        debug('\n' + config_block)
        append_configfile(config_block)
        write_blocks += 1

    info('Wrote ' + str(write_blocks) + ' hostGroups objects')
