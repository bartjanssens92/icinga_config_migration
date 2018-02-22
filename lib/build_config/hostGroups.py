from lib.general import *
from lib.build_hash import build_hash

def config():
    render_hostGroups(build_hash('hostgroup'))

def render_hostGroups(object_hash):
    """

    """

    # Header
    write_configfile(settings.header)

    # Defaults
    write_blocks = 0

    for hostGroups in object_hash:

        # Init config block
        config_block = ''

        # Write configblock
        append_configfile(config_block)
        write_blocks += 1

    info('Wrote ' + str(write_blocks) + ' hostGroups objects')
