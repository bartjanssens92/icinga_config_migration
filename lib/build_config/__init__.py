from lib.general import *

# 3 hard things in IT, naming is causing this mess
import hosts as hosts_
import hostTemplates as hostTemplates_
import hostGroups as hostGroups_
import services as services_
import serviceTemplates as serviceTemplates_
import serviceGroups as serviceGroups_
import commands as commands_
import contacts as contacts_
#import hosts as hosts_
#import hosts as hosts_

# Wrappers
def hosts():
    hosts_.config()

def hostTemplates():
    hostTemplates_.config()

def hostGroups():
    hostGroups_.config()

def services():
    services_.config()

def serviceTemplates():
    serviceTemplates_.config()

def serviceGroups():
    serviceGroups_.config()

def commands():
    commands_.config()

def contacts():
    contacts_.config()
