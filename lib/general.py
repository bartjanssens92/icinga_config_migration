import sys
import settings

def error(message):
    """Function for echoing errors and exiting"""
    print('ERROR: ' + str(message))
    sys.exit(1)

def info(message):
    """Function for echoing debug"""
    print('INFO: ' + str(message))

def debug(message):
    """Function for echoing debug"""
    if settings.debug:
        print('DEBUG: ' + str(message))

def debug3(message):
    """Function for echoing debug"""
    if settings.debug3:
        print('DEBUG: ' + str(message))

def write_configfile(block):
    #filelocation = settings.outputdir + settings.object_name + '.conf'
    filelocation = settings.outputfile
    info('Wrote header to ' + filelocation )
    fh = open(filelocation, 'w+')
    fh.write(block)
    fh.close

def append_configfile(block):
    #filelocation = settings.outputdir + settings.object_name + '.conf'
    filelocation = settings.outputfile
    debug('Wrote configblock to ' + filelocation)
    fh = open(filelocation, 'a')
    fh.write(block)
    fh.close

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
