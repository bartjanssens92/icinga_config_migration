#!/usr/bin/python2.7
from lib import settings
from lib import parse_arguments
from lib.general import debug
from lib import build_icinga_config
"""
Main entry point for generating the icinga2 compatible config.

Need to add examples and more information on how to use this utility.
"""
def main():
    parse_arguments
    build_icinga_config

if __name__ == "__main__":
    main()
