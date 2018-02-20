#!/usr/bin/python2.7
from convert_lib.general import info,error,write_configfile,append_configfile
from convert_lib.general import debug as debug_general

def debug(msg):
    """
    Function to enable per-object debugging.
    """
    param_debug = False
    if param_debug:
        debug_general(msg)

def build_host_notification_hash(object_type, object_hash, contact_hash):
    """Function to get a hash of contacts and contactgroups by notification method"""
    notification_type = str(object_type) + '_notification_commands'
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
                if notification_method in ['host-notify-by-email']:
                    notification_hash['mail']['users'].append(contact)
                elif notification_method in ['host_notify_by_sms']:
                    notification_hash['sms']['users'].append(contact)
                else:
                    notification_hash['unmatched']['users'].append(contact)

        else:
            notification_method = contact_hash[object_hash['contacts']][notification_type]
            if notification_method in ['host-notify-by-email']:
                notification_hash['mail']['users'].append(object_hash['contacts'])
            elif notification_method in ['host_notify_by_sms']:
                notification_hash['sms']['users'].append(object_hash['contacts'])
            else:
                notification_hash['unmatched']['users'].append(contact)
    # Contactgroups
    if 'contact_groups' in object_hash:
        # Check if there are multiple contacts defind
        # Contactgroups always get emailed
        if isinstance(object_hash['contact_groups'], list):
            for contact in object_hash['contact_groups']:
                notification_hash['mail']['groups'].append(contact)
        else:
            notification_hash['mail']['groups'].append(object_hash['contact_groups'])

    debug(notification_hash)
    return notification_hash
