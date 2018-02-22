import sys
import settings

def error(message):
    """
    Function to print error messages and then exit.
    """
    print('ERROR: ' + str(message))
    sys.exit(1)

def info(message):
    """
    Function for printing info messages.
    """
    print('INFO: ' + str(message))

def debug(message):
    """
    Function for printing debug messages. ( level 1 )
    Used for object debugging.
    """
    if settings.debug:
        print('DEBUG: ' + str(message))

def debug2(message):
    """
    Function for printing debug messages. ( level 2 )
    Not used atm.
    """
    if settings.debug2:
        print('DEBUG: ' + str(message))

def debug3(message):
    """
    Function for printing debug messages. ( level 3 )
    Used for hash debugging, printing hash key, values in a for loop.
    """
    if settings.debug3:
        print('DEBUG: ' + str(message))

def debug4(message):
    """
    Function for printing debug messages. ( level 4 )
    Used for build_hash debugging.
    """
    if settings.debug4:
        print('DEBUG: ' + str(message))

def write_configfile(block):
    """
    Function for creating the outputfile and writing the header to it.
    """
    info('Wrote header to ' + settings.outputfile)
    fh = open(filelocation, 'w+')
    fh.write(block)
    fh.close

def append_configfile(block):
    """
    Function for appending configblocks to the outputfile.
    """
    debug('Wrote configblock to ' + settings.outputfile)
    fh = open(filelocation, 'a')
    fh.write(block)
    fh.close

def is_number(s):
    """
    Function to check if a number is not a string.
    """
    try:
        float(s)
        return True
    except ValueError:
        return False
