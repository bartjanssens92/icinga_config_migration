from lib.general import *
from lib.build_hash import build_hash

def render(object_hash):
    """
    Function to build the serviceGroup object, same as for user, service and services.
    object HostGroup "hg1" {
      assign where service.name in [ "service1", "service2" ]
    }

    object HostGroup "hg2" {
      groups = [ "hg1" ]
      assign where service.name == "service3"
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
        config_block = 'object ServiceGroup "' + servicegroup_hash['servicegroup_name'] + '" {\n'
        # Hostgroup members
        if 'servicegroup_members' in servicegroup_hash and len(servicegroup_hash['servicegroup_members']) > 1:
            config_block += ' groups = [" ' + '", "'.join(servicegroup_hash['servicegroup_members']) + '" ]\n'
        elif 'servicegroup_members' in servicegroup_hash:
            config_block += ' groups = [" ' + servicegroup_hash['servicegroup_members'] + '" ]\n'
        # Get members
        config_block += '  assign where service.name in [ "' + '", "'.join(servicegroup_hash['members']) + '" ]\n'

        # Close the config block
        config_block += '}\n'

        # Write configblock
        debug('\n' + config_block)
        append_configfile(config_block)
        write_blocks += 1

    info('Wrote ' + str(write_blocks) + ' serviceGroups objects')
