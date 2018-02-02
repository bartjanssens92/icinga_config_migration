def error(message):
    """Function for echoing errors and exiting"""
    print('ERROR: ' + str(message))
    sys.exit(1)

def info(message):
    """Function for echoing debug"""
    print('INFO: ' + str(message))

def debug(message):
    """Function for echoing debug"""
    debug = True
    if debug:
        print('DEBUG: ' + str(message))

def write_configfile(block,filelocation):
    info('Wrote header to ' + filelocation)
    fh = open(filelocation, 'w+')
    fh.write(block)
    fh.close

def append_configfile(block,filelocation):
    info('Wrote configblock to ' + filelocation)
    fh = open(filelocation, 'a')
    fh.write(block)
    fh.close

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
