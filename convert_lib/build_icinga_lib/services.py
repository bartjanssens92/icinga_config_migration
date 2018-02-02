#!/usr/bin/python2.7
from convert_lib.general import debug,info,error,write_configfile,append_configfile

def build_icinga_services(object_hash,outputfile):
    """Function to build the icinga services config file:
apply Service "service1" {
  import "generic-service"
  check_command = "test_check"

  assign where host.name in [ "localhost1", "localhost2" ]
  vars.argument = "test"
}
    """
    #Defaults

    for service in object_hash:
        debug('--------------------')
        debug(service)
        for host in object_hash[service]['hosts']:
            debug('====================')
            debug(host)
            #debug(object_hash[service]['hosts'][host])
            if 'check_command' in object_hash[service]['hosts'][host]:
                debug(object_hash[service]['hosts'][host]['check_command'])
#                arguments = 

    # Header
    header = '# File generated by script, do not edit!\n'
    write_configfile(header, outputfile)