#!/usr/bin/python2.7
from lib.general import *

def convert_options(options_list):
    """
    Function to convert notification_options into state and type configuration.
    Following the table described here: https://www.icinga.com/docs/icinga2/latest/doc/23-migrating-from-icinga-1x/#manual-config-migration-hints-for-notification-filters
    """
    state = []
    types = ['Custom','Problem']
    for option in options_list:
        if option == 'o':
            state.append('OK')
        elif option == 'w':
            state.append('Warning')
        elif option == 'c':
            state.append('Critical')
        elif option == 'u':
            state.append('Unknown')
        elif option == 'd':
            state.append('Down')
        elif option == 's':
            types.append('DowntimeStart')
            types.append('DowntimeEnd')
            types.append('DowntimeRemoved')
        elif option == 'r':
            state.append('OK')
            types.append('Recovery')
        elif option == 'f':
            types.append('FlappingStart')
            types.append('FlappingEnd')
        elif option == 'n':
            state.append('0')
            types.append('0')

    return state,types

def convert_macro(macro):
    """
    Function to convert macros from the old style to the new one
    Following the table described here: https://www.icinga.com/docs/icinga2/latest/doc/23-migrating-from-icinga-1x/#differences-1x-2-runtime-macros
    """
    convert_dict = {
    'CONTACTNAME'                    : 'user.name',
    'CONTACTALIAS'                   : 'user.display_name',
    'CONTACTEMAIL'                   : 'user.email',
    'CONTACTPAGER'                   : 'user.pager',
    'SERVICEDESC'                    : 'service.name',
    'SERVICEDISPLAYNAME'             : 'service.display_name',
    'SERVICECHECKCOMMAND'            : 'service.check_command',
    'SERVICESTATE'                   : 'service.state',
    'SERVICESTATEID'                 : 'service.state_id',
    'SERVICESTATETYPE'               : 'service.state_type',
    'SERVICEATTEMPT'                 : 'service.check_attempt',
    'MAXSERVICEATTEMPT'              : 'service.max_check_attempts',
    'LASTSERVICESTATE'               : 'service.last_state',
    'LASTSERVICESTATEID'             : 'service.last_state_id',
    'LASTSERVICESTATETYPE'           : 'service.last_state_type',
    'LASTSERVICESTATECHANGE'         : 'service.last_state_change',
    'SERVICEDOWNTIME'                : 'service.downtime_depth',
    'SERVICEDURATIONSEC'             : 'service.duration_sec',
    'SERVICELATENCY'                 : 'service.latency',
    'SERVICEEXECUTIONTIME'           : 'service.execution_time',
    'SERVICEOUTPUT'                  : 'service.output',
    'SERVICEPERFDATA'                : 'service.perfdata',
    'LASTSERVICECHECK'               : 'service.last_check',
    'SERVICENOTES'                   : 'service.notes',
    'SERVICENOTESURL'                : 'service.notes_url',
    'SERVICEACTIONURL'               : 'service.action_url',
    'HOSTNAME'                       : 'host.name',
    'HOSTADDRESS'                    : 'host.address',
    'HOSTADDRESS6'                   : 'host.address6',
    'HOSTDISPLAYNAME'                : 'host.display_name',
    'HOSTALIAS'                      : 'host.display_name',
    'HOSTCHECKCOMMAND'               : 'host.check_command',
    'HOSTSTATE'                      : 'host.state',
    'HOSTSTATEID'                    : 'host.state_id',
    'HOSTSTATETYPE'                  : 'host.state_type',
    'HOSTATTEMPT'                    : 'host.check_attempt',
    'MAXHOSTATTEMPT'                 : 'host.max_check_attempts',
    'LASTHOSTSTATE'                  : 'host.last_state',
    'LASTHOSTSTATEID'                : 'host.last_state_id',
    'LASTHOSTSTATETYPE'              : 'host.last_state_type',
    'LASTHOSTSTATECHANGE'            : 'host.last_state_change',
    'HOSTDOWNTIME'                   : 'host.downtime_depth',
    'HOSTDURATIONSEC'                : 'host.duration_sec',
    'HOSTLATENCY'                    : 'host.latency',
    'HOSTEXECUTIONTIME'              : 'host.execution_time',
    'HOSTOUTPUT'                     : 'host.output',
    'HOSTPERFDATA'                   : 'host.perfdata',
    'LASTHOSTCHECK'                  : 'host.last_check',
    'HOSTNOTES'                      : 'host.notes',
    'HOSTNOTESURL'                   : 'host.notes_url',
    'HOSTACTIONURL'                  : 'host.action_url',
    'TOTALSERVICES'                  : 'host.num_services',
    'TOTALSERVICESOK'                : 'host.num_services_ok',
    'TOTALSERVICESWARNING'           : 'host.num_services_warning',
    'TOTALSERVICESUNKNOWN'           : 'host.num_services_unknown',
    'TOTALSERVICESCRITICAL'          : 'host.num_services_critical',
    'COMMANDNAME'                    : 'command.name',
    'NOTIFICATIONTYPE'               : 'notification.type',
    'NOTIFICATIONAUTHOR'             : 'notification.author',
    'NOTIFICATIONCOMMENT'            : 'notification.comment',
    'NOTIFICATIONAUTHORNAME'         : 'notification.author',
    'NOTIFICATIONAUTHORALIAS'        : 'notification.author',
    'TIMET'                          : 'icinga.timet',
    'LONGDATETIME'                   : 'icinga.long_date_time',
    'SHORTDATETIME'                  : 'icinga.short_date_time',
    'DATE'                           : 'icinga.date',
    'TIME'                           : 'icinga.time',
    'PROCESSSTARTTIME'               : 'icinga.uptime',
    'TOTALHOSTSUP'                   : 'icinga.num_hosts_up',
    'TOTALHOSTSDOWN'                 : 'icinga.num_hosts_down',
    'TOTALHOSTSUNREACHABLE'          : 'icinga.num_hosts_unreachable',
    'TOTALHOSTSDOWNUNHANDLED'        : '-',
    'TOTALHOSTSUNREACHABLEUNHANDLED' : '-',
    'TOTALHOSTPROBLEMS'              : 'down',
    'TOTALHOSTPROBLEMSUNHANDLED'     : 'down-(downtime+acknowledged)',
    'TOTALSERVICESOK'                : 'icinga.num_services_ok',
    'TOTALSERVICESWARNING'           : 'icinga.num_services_warning',
    'TOTALSERVICESCRITICAL'          : 'icinga.num_services_critical',
    'TOTALSERVICESUNKNOWN'           : 'icinga.num_services_unknown',
    'TOTALSERVICESWARNINGUNHANDLED'  : '-',
    'TOTALSERVICESCRITICALUNHANDLED' : '-',
    'TOTALSERVICESUNKNOWNUNHANDLED'  : '-',
    'TOTALSERVICEPROBLEMS'           : 'ok+warning+critical+unknown',
    'TOTALSERVICEPROBLEMSUNHANDLED'  : 'warning+critical+unknown-(downtime+acknowledged)',
    'CHANGE_CUSTOM_CONTACT_VAR'      : 'CHANGE_CUSTOM_USER_VAR',
    }

    # Strip the $$
    sane_macro = macro.translate(None, '$')
    #debug(sane_macro)
    if not sane_macro in convert_dict:
        return ''
    else:
        return '$' + convert_dict[sane_macro] + '$'


"""
#The following external commands are not supported:
CHANGE_*MODATTR
CHANGE_CONTACT_HOST_NOTIFICATION_TIMEPERIOD
CHANGE_HOST_NOTIFICATION_TIMEPERIOD
CHANGE_SVC_NOTIFICATION_TIMEPERIOD
DEL_DOWNTIME_BY_HOSTGROUP_NAME
DEL_DOWNTIME_BY_START_TIME_COMMENT
DISABLE_ALL_NOTIFICATIONS_BEYOND_HOST
DISABLE_CONTACT_HOST_NOTIFICATIONS
DISABLE_CONTACT_SVC_NOTIFICATIONS
DISABLE_CONTACTGROUP_HOST_NOTIFICATIONS
DISABLE_CONTACTGROUP_SVC_NOTIFICATIONS
DISABLE_FAILURE_PREDICTION
DISABLE_HOST_AND_CHILD_NOTIFICATIONS
DISABLE_HOST_FRESHNESS_CHECKS
DISABLE_NOTIFICATIONS_EXPIRE_TIME
DISABLE_SERVICE_FRESHNESS_CHECKS
ENABLE_ALL_NOTIFICATIONS_BEYOND_HOST
ENABLE_CONTACT_HOST_NOTIFICATIONS
ENABLE_CONTACT_SVC_NOTIFICATIONS
ENABLE_CONTACTGROUP_HOST_NOTIFICATIONS
ENABLE_CONTACTGROUP_SVC_NOTIFICATIONS
ENABLE_FAILURE_PREDICTION
ENABLE_HOST_AND_CHILD_NOTIFICATIONS
ENABLE_HOST_FRESHNESS_CHECKS
ENABLE_SERVICE_FRESHNESS_CHECKS
READ_STATE_INFORMATION
SAVE_STATE_INFORMATION
SET_HOST_NOTIFICATION_NUMBER
SET_SVC_NOTIFICATION_NUMBER
START_ACCEPTING_PASSIVE_HOST_CHECKS
START_ACCEPTING_PASSIVE_SVC_CHECKS
START_OBSESSING_OVER_HOST
START_OBSESSING_OVER_HOST_CHECKS
START_OBSESSING_OVER_SVC
START_OBSESSING_OVER_SVC_CHECKS
STOP_ACCEPTING_PASSIVE_HOST_CHECKS
STOP_ACCEPTING_PASSIVE_SVC_CHECKS
STOP_OBSESSING_OVER_HOST
STOP_OBSESSING_OVER_HOST_CHECKS
STOP_OBSESSING_OVER_SVC
STOP_OBSESSING_OVER_SVC_CHECKS
"""
