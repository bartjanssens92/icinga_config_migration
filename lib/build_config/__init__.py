from lib.general import *
from lib.build_hash import build_hash

import hosts
import hostTemplates
import hostGroups
import services
import serviceTemplates
import serviceGroups
import commands
import contacts
import resource

def actions(object_name, contact_hash):
    """
    @TODO : Add something here
    Passing the contact_hash so that every object doesn't need to generate it.
    """
    settings.outputfile = settings.outputdir + object_name + '.conf'

    # Depending on the object type different actions need to be taken
    if object_name in ['host']:
        hosts.render(build_hash(object_name), contact_hash)
    elif object_name in ['hostTemplate']:
        hostTemplates.render(build_hash(object_name), contact_hash)
    elif object_name in ['hostgroup']:
        hostGroups.render(build_hash(object_name))
    elif object_name in ['service']:
        services.render(build_hash(object_name), commands.get_hash(), serviceTemplates.get_hash(), contact_hash)
    elif object_name in ['serviceTemplate']:
        serviceTemplates.render(build_hash(object_name), commands.get_hash(), contact_hash)
    elif object_name in ['servicegroup']:
        serviceGroups.render(build_hash(object_name))
    elif object_name in ['command']:
        commands.render(build_hash(object_name))
    elif object_name in ['contact']:
        contacts.render(contact_hash, build_hash('contactgroup'))
    elif object_name in ['resource']:
        resource.render()
    # @TODO: Render lists of what contact gets what notifications?
    #elif object_name in ['notification']:
    #    build_icinga_notifications(inputdir,outputfile)
    elif object_name in ['all']:
        for object_n in settings.objects_all:
            info('Building configuration for: ' + object_n)
            actions(object_n, contact_hash)
            info('')

actions(settings.object_name, build_hash('contact'))
