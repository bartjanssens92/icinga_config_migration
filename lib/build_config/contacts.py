#!/usr/bin/python2.7
import lib.settings
from lib.general import *
from lib.build_hash import build_hash

def config():
    render_contacts(build_hash('contact'), build_hash('contactgroup'))

def render_contacts(object_hash, groups_hash):
    """Function to build the users:
object User "testconfig-user" {
  import "generic-user"
  display_name = "Icinga Test User"
  email = "icinga@localhost"
}

object UserGroup "icingaadmins" {
  display_name = "Icinga 2 Admin Group"
}   """
    # Default
    write_contact_blocks = 0
    write_group_blocks = 0

    # Header
    write_configfile(settings.header)

    # Loop over the templates
    for contact in object_hash:
        debug('--------------------')
        debug(contact)
        debug(object_hash[contact])

        # Build the config block
        config_block = 'object User "' + contact + '" {\n'
        config_block += '  import "generic-user"\n'
        config_block += '  display_name = "' + object_hash[contact]['alias'] + '"\n'
        config_block += '  email = "' + object_hash[contact]['email'] + '"\n'

        # Get the groups of the user
        contact_group = []
        for group in groups_hash:
            if contact in groups_hash[group]['members']:
                contact_group.append(group)
                debug('Found contact in: ' + group)
        if not contact_group == []:
            config_block += '  groups = [ "' + '", "'.join(contact_group) + '" ]\n'
        else:
            pass

        # Close config block
        config_block += '}\n'

        debug('\n' + config_block)
        append_configfile(config_block)
        write_contact_blocks += 1

    info('Wrote ' + str(write_contact_blocks) + ' contact objects')
    append_configfile('# Groups\n')

    # Also build the contactgroups
    for group in groups_hash:
        config_block = 'object UserGroup "' + group + '" {\n'
        config_block += '  display_name = "' + groups_hash[group]['alias'] + '"\n'
        config_block += '}\n'
        debug('\n' + config_block)
        append_configfile(config_block)
        write_group_blocks += 1

    info('Wrote ' + str(write_group_blocks) + ' group objects')

