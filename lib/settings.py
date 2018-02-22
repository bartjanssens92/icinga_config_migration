# Settings file
#
# The location of the centreon config
inputdir = '/home/bjanssens/Documents/centreon/original/centreon-engine/'
#inputdir = '/mnt/home/bjanssens/Documents/centreon/original/centreon-engine/'
# The location of the output
outputdir = '/home/bjanssens/Documents/centreon/converted/'
#outputdir = '/mnt/home/bjanssens/Documents/centreon/converted/'
# The header in the config files
header = '# File build by script, DO NOT MODIFY!\n'
# Depricated, Parameter to enable file writing
write = False
# Object names
object_name = 'all'
objects_all = ['host','service','serviceTemplate','contact','hostgroup','servicegroup','hostTemplate','command','notification']
# Declaring an empty outputfile
outputfile = ''
# Debug levels
debug = False
debug3 = False
