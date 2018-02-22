# Custom libs
import settings
import build_config
from general import *

def actions(object_name):
    """
    @TODO : Add something here
    """
    settings.outputfile = settings.outputdir + object_name + '.conf'

    # Depending on the object type different actions need to be taken
    if object_name in ['host']:
        build_config.hosts()
    elif object_name in ['hostTemplate']:
        build_config.hostTemplates()
    elif object_name in ['hostgroup']:
        build_config.hostGroups()
    elif object_name in ['service']:
        build_config.services()
    elif object_name in ['serviceTemplate']:
        build_config.serviceTemplates()
    elif object_name in ['servicegroup']:
        build_config.serviceGroups()
    elif object_name in ['command']:
        build_config.commands()
    elif object_name in ['contact']:
        build_config.contacts()
    #elif object_name in ['notification']:
    #    build_icinga_notifications(inputdir,outputfile)
    elif object_name in ['all']:
        for object_n in settings.objects_all:
            info('Building configuration for: ' + object_n)
            actions(object_n)
            info('')

actions(settings.object_name)

