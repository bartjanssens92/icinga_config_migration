#!/usr/bin/python2.7
from collections import OrderedDict
# Custom stuff
from lib.general import *
from lib.build_hash import build_hash
from convert import convert_options

def build_notification_contacts(object_type, object_hash, contact_hash):
    """
    Function to get a hash of contacts and contactgroups by notification method
    """
    debug('Object_type: ' + object_type)
    # Nagios config defines them in the contacts with the keys (service|host)_notification_commands
    notification_type = str(object_type) + '_notification_commands'
    # Build the notification_hash
    notification_hash = {
        'mail' : {
            'users' : [],
            'groups' : [],
        },
        'sms' : {
            'users' : [],
            'groups' : [],
        },
        'unmatched' : {
            'users' : [],
            'groups' : [],
        },
    }
    # Contacts
    if 'contacts' in object_hash:
        # Check if there are multiple contacts defind
        if isinstance(object_hash['contacts'], list):
            for contact in object_hash['contacts']:
                notification_method = contact_hash[contact][notification_type]
                debug('Notification method: ' + notification_method)
                # Put each one in the correct group
                if notification_method in ['host-notify-by-email','service-notify-by-email']:
                    notification_hash['mail']['users'].append(contact)
                elif notification_method in ['host_notify_by_sms','service-notify_by_sms']:
                    notification_hash['sms']['users'].append(contact)
                else:
                    notification_hash['unmatched']['users'].append(contact)
        else:
            notification_method = contact_hash[object_hash['contacts']][notification_type]
            # Put it in the correct group
            if notification_method in ['host-notify-by-email','service-notify-by-email']:
                notification_hash['mail']['users'].append(object_hash['contacts'])
            elif notification_method in ['host_notify_by_sms','service-notify_by_sms']:
                notification_hash['sms']['users'].append(object_hash['contacts'])
            else:
                notification_hash['unmatched']['users'].append(object_hash['contacts'])

    # Contactgroups
    if 'contact_groups' in object_hash:
        # Check if there are multiple contacts defined
        # Contactgroups always get emailed
        if isinstance(object_hash['contact_groups'], list):
            for contact in object_hash['contact_groups']:
                notification_hash['mail']['groups'].append(contact)
        else:
            notification_hash['mail']['groups'].append(object_hash['contact_groups'])

    debug3('Notification hash: ' + str(notification_hash))

    # Build the configuration blocks
    config_block = ''

    # Mail
    # Check if they aren't empty
    if notification_hash['mail']['users'] or notification_hash['mail']['groups']:
        config_block += '  vars.notification["mail"] = {\n'
        # Check if there are any groups defined
        if notification_hash['mail']['groups'] != []:
            # If there are multiple groups defined, join them with the correct format
            if len(notification_hash['mail']['groups']) > 1:
                config_block += '    groups = [ "' + '", "'.join(notification_hash['mail']['groups']) + '" ]\n'
            # Otherwise just add the group
            else:
                config_block += '    groups = [ "' + str(notification_hash['mail']['groups'][0]) + '" ]\n'
        # Check if there are any users defined
        if notification_hash['mail']['users'] != []:
            # If there are multiple groups defined, join them with the correct format
            if len(notification_hash['mail']['users']) > 1:
                config_block += '    users = [ "' + '", "'.join(notification_hash['mail']['users']) + '" ]\n'
            # Otherwise just add the user
            else:
                config_block += '    users = [ "' + str(notification_hash['mail']['users'][0]) + '" ]\n'
        # Close the mail notification block
        config_block += '  }\n\n'

    # SMS
    # Check if they aren't empty
    if notification_hash['sms']['users'] or notification_hash['sms']['groups']:
        config_block += '  vars.notification["sms"] = {\n'
        if notification_hash['sms']['groups'] != []:
            if len(notification_hash['sms']['groups']) > 1:
                config_block += '    groups = [ "' + '"," '.join(notification_hash['sms']['groups']) + '"]\n'
            else:
                config_block += '    groups = [ "' + str(notification_hash['sms']['groups'][0]) + ' "]\n'
        if notification_hash['sms']['users'] != []:
            if len(notification_hash['sms']['users']) > 1:
                config_block += '    users = [ "' + '"," '.join(notification_hash['sms']['users']) + '"]\n'
            else:
                config_block += '    users = [ "' + str(notification_hash['sms']['users'][0]) + ' "]\n'
        # Close the sms notification block
        config_block += '  }\n\n'

    return config_block

def render_notifications(object_hash,contact_hash,notif_type='host'):
    """
    Function to build notifiction config blocks.
    Usefull as every object uses the same parameters for defining variables.
    """
    # Defaults
    config_block = ''

    # Contacts
    config_block += build_notification_contacts(notif_type, object_hash, contact_hash)

    # Notification states and types
    if 'notification_options' in object_hash:
        states, types = convert_options(object_hash['notification_options'])
        config_block += '  vars.notification["states"] = [ ' + ', '.join(states) + ' ]\n'
        config_block += '  vars.notification["types"] = [ ' + ', '.join(types) + ' ]\n'

    # Other notification params
    if 'notification_period' in object_hash:
        config_block += '  vars.notification["period"] = "' + object_hash['notification_period'] + '"\n'
    if 'notification_interval' in object_hash:
        config_block += '  vars.notification["interval"] = ' + object_hash['notification_interval'] + 's\n'
    if 'notifications_enabled' in object_hash:
        config_block += '  vars.notification["enabled"] = "' + object_hash['notifications_enabled'] + '"\n'

    # Return the block
    return config_block

def build_icinga_notifications(inputdir,outputfile):
    """
    Function to build notification objects.
    object Notification "<notificationname>" {
      import "mail-host-notification"
      host_name = "<thishostname>"
      command = "<notificationcommandname>"
      states = [ OK, Warning, Critical ]
      types = [ Recovery, Problem, Custom ]
      period = "24x7"
      users = [ "<contactwithnotificationcommand>" ]
    }
    """
    # Header
    header = '# File generated by script, do not edit!\n'
    write_configfile(header, outputfile)

    #Defaults
    write_blocks = 0
    service_notifications = OrderedDict({})
    host_notifications = OrderedDict({})

    # Get the needed hashes
    host_hash = build_hash('host',inputdir)
    hosttemplate_hash = build_hash('hostTemplate', inputdir)
    service_hash = build_hash('service',inputdir)
    servicetemplate_hash = build_hash('serviceTemplate',inputdir)

    for service in service_hash:
        debug('--------------------')
        debug(service)
        debug('--------------------')
        #debug_3(service_hash[service])

        # Setup the notifications hash
        sane_service = service.replace('!','_').replace('/','').replace('"','')
        service_notifications[sane_service] = OrderedDict({})
        service_notifications[sane_service]['host'] = service_hash[service]['config']['host_name']

        # Get some contact information
        if 'contacts' in service_hash[service]['config']:
            service_notifications[sane_service]['contacts'] = service_hash[service]['config']['contacts']
        if 'contact_groups' in service_hash[service]['config']:
            service_notifications[sane_service]['contact_groups'] = service_hash[service]['config']['contact_groups']
        if 'notification_period' in service_hash[service]['config']:
            service_notifications[sane_service]['notification_period'] = service_hash[service]['config']['notification_period']
        if 'notification_interval' in service_hash[service]['config']:
            service_notifications[sane_service]['notification_interval'] = service_hash[service]['config']['notification_interval']
        if 'notification_options' in service_hash[service]['config']:
            state, types = convert_options(service_hash[service]['config']['notification_options'])
            service_notifications[sane_service]['state'] = state
            service_notifications[sane_service]['type'] = types
        if 'notifications_enabled' in service_hash[service]['config']:
            service_notifications[sane_service]['notifications_enabled'] = service_hash[service]['config']['notifications_enabled']

        # Print all the collected attributes
        for key in service_notifications[sane_service]:
            debug(key + ' : ' + str(service_notifications[sane_service][key]))


    for host in host_hash:
        debug('--------------------')
        debug(host)
        debug('--------------------')
        #debug_3(host_hash[host])

        # Setup the notifications hash
        sane_host = host
        host_notifications[host] = OrderedDict({})

        #Form a list of all the contacts involved
        if 'contacts' in host_hash[host]:
            host_notifications[sane_host]['contacts'] = host_hash[host]['contacts']
        if 'contact_groups' in host_hash[host]:
            host_notifications[sane_host]['contact_groups'] = host_hash[host]['contact_groups']
        if 'notification_period' in host_hash[host]:
            host_notifications[sane_host]['notification_period'] = host_hash[host]['notification_period']
        if 'notification_interval' in host_hash[host]:
            host_notifications[sane_host]['notification_interval'] = host_hash[host]['notification_interval']
        if 'notification_options' in host_hash[host]:
            state, types = convert_options(host_hash[host]['notification_options'])
            host_notifications[sane_host]['state'] = state
            host_notifications[sane_host]['type'] = types
        if 'notifications_enabled' in host_hash[host]:
            host_notifications[sane_host]['notifications_enabled'] = host_hash[host]['notifications_enabled']

        # Print all the collected attributes
        for key in host_notifications[sane_host]:
            debug(key + ' : ' + str(host_notifications[sane_host][key]))



#        # Close the config_block
#        config_block += '}\n'
#
#        # Print the config in the config file
#        debug("\n" + config_block)
#        append_configfile(config_block, outputfile)
#        write_blocks += 1

#    info('Wrote ' + str(write_blocks) + ' notification objects')

