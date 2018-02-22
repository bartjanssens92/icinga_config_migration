from lib.general import *
from lib.build_hash import build_hash

# Template, replace objectN with correct name

def config():
    render_objectN(build_hash('objectN')

def render_objectN(object_hash):
    """

    """

    # Header
    write_configfile(settings.header)

    # Defaults
    write_blocks = 0

    for objectN in object_hash:

        # Init config block
        config_block = ''

        # Write configblock
        append_configfile(config_block)
        write_blocks += 1

    info('Wrote ' + str(write_blocks) + ' objectN objects')
