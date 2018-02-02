# Icinga1.x to Icinga2.x configuration

This collection of python scripts can be used to convert Icinga1.x configuration objects into Icinga2 objects.

## Scope

The scope of this project is for the script to be pointed to a Icinga1.x configuration directory and convert it into an Icinga2 configuration.
This means that the generated output of this script must pass the Icinga2 config validator. ( icinga2 deamon --validate ).
It does not mean that the generated config will 100% match the behavior of the old config.

## What works

- Hosts
- HostTemplates
- Commands
- Users
- Usergroups

## What doesn't work (yet)

- Services
- Notifications

## How to use

```
~# ./convert.py -o <object name>
```

## Todo

- Get the debugging flag working properly.
- Setup some more decent directories.
- Cleanup commented code.
- Document code better.
