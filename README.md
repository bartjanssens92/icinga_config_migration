# Icinga1.x to Icinga2.x configuration

This collection of python scripts can be used to convert Icinga1.x configuration objects into Icinga2 objects.

## Scope

The scope of this project is for the script to be pointed to a Icinga1.x configuration directory and convert it into an Icinga2 configuration.
This means that the generated output of this script must pass the Icinga2 config validator. ( icinga2 deamon --validate ).
It does not mean that the generated config will 100% match the behavior of the old config.

## What works

- Hosts
- HostTemplates
- Hostgroups
- Services
- ServiceTemplates
- Servicegroups
- Users
- Usergroups
- Commands
- Notifications

## What doesn't work (yet)

- Commands assume they are all installed in the same place
- Build_hash is unable to work with multilines

## How to use

```
Usage: ./main.py [OPTIONS]

  -h, --help    Show help
  -w, --write   (Depricated) Write the configfiles
  -d, --debug   Enable debugging ( level 1 )
  -o, --object=   Generate only the configuration of this object
  -I, --input=    Use this directoy as input
  -O, --output=   Which directory to write the configfiles in

Examples:

* Generate configuration for all the objects:
  ./main.py
* Generate configuration for the host object:
  ./main.py -o host
* Generate configuration from /tmp/in:
  ./main.py -I /tmp/in

```

## Todo

- Bugfix: Add hostparameters to the hosts as they are currently ignored.
  Ex:
```
define host {
    hostname          some.host.name
    _SNMPCOMMUNITY    public
    _SNMPVERSION      2c
    ...
}
```

Should generate:

```
object Host "some.host.name" {
  ...
  vars.snmpcommunity = "public"
  vars.snmpversion = "2c"

}
```

The check_command object should also not ignore these parameters.

- Bugfix: SNMP service not passing the -o option correctly.
- Bugfix: Parameters from the resource.cfg are not passed, these should be constants:

```
const Name = "value"
```

- Get the debugging flag working properly.
- See @TODO lines in code
