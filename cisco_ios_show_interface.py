"""
Simple script that parses through Cisco IOS 'show interface' output and prints certain lines that match search filter.
The output is somewhere equivalent to using pipe with show command, e.g 'show interface | include tunnel|Description|Internet'.
"""
__author__ = 'mmussin'

import os
import sys
import re

def get_file_lines(pipe_text='', file_name=''):
    # Open file in read only mode and read text lines into list with new line and space characters stripped
    file_lines = [line.strip() for line in open(file_name, 'r')]
    return file_lines

def get_intf_info(reg_exp, file_name):
    # Python's 're' Regular Expression module can be used for matching and searching operations
    file_line = get_file_lines('', file_name)

    # I guess instead of loop statement, this printout operation could be written in more 'Pythonic' way something like this
    # 'print '\n'.join([x for x in file_line if re.match(reg_exp, x, re.IGNORECASE)])'
    for x in file_line:
        if re.match(reg_exp, x, re.IGNORECASE): print x

def main(filter, file):
	get_intf_info(filter, file)

if __name__ == '__main__':
    # You have an option to either use your own command line arguments for RegEx filter and filename and its path or simply
    # launch the script without any arguments, in which case the default RegEx filter and full filename will be used
	try:
		main(sys.argv[1], sys.argv[2])
	except:
		main(filter = 'loopback[0-9]|tunnel[0-9]|description|internet address|mtu', file = '/tmp/showoutput.log')
		print '\nThis is default filter and filename... '
