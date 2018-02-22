#!/usr/bin/python2.7
from lib import parse_arguments
from lib import build_config
"""
Main entry point for generating the icinga2 compatible config.

Need to add examples and more information on how to use this utility.
"""
def main():
    parse_arguments
    build_config

if __name__ == "__main__":
    main()
