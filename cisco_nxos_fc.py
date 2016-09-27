'''
After upgrading old Cisco MDS Fiber Channel switches with Cisco Nexus 5548 UP, I had to start supporting FC storage
configuration. We didn't have any management software like Cisco DC Prime that manages these kind of tasks and standard
Cisco way is to use NX-OS CLI to configure FC zoning which is very tedious. Thankfully, the tickets that I was receiving
from storage team were coming as formatted text files. So it was relatively easy to write simple script that parses through
text file, formats some fields and generates output files that are ready to be paste into switch console.

Example:

nx-fc.py in.txt out.txt out_zones.txt out_zoneset.txt

in.txt:
SQLSRV01A	A0:03:FF:4F:1B:57:02:30	A:1:A:2:A3:A4:A5:A:6:A:7A:8	B1B2B3B4B5B6B7B8
		A003FF4F1B570231	A1A2A3A4A5A6A7A8	B1B2B3B4B5B6B7B8
		A0:03:FF:4F:1B:57:02:32	A1A2A3A4A5A6A7A8	B1-B2B3B4B5B6B7B8
		A0:03:FF:4F:1B:57:02:33	A1A2A3A4A5A6A7A8	B1:B2:B3B4B5B6B7B8

SQLSERV02A		B003;FF4F1B570250	C1C2C3C4C5C6C7C8	D1D2D3D4D5D6D7D8
		B0:03:FF:4F:1B:57:02-51	C1C2C3C4C5C6C7C8	D1D2D3D4D5D6D7D8
		B0:03-FF:4F:1B:5702;52	C1C2C3C4C5C6C7C8	D1D2D3D4D5D6D7D8
		B:0,0-3FF4F-1B.5.7:02:53	C1C2C3C4C5C6C7C8	D1D2D3D4D5D6D7D8

out.txt:
SQLSRV01A_Z1 A0:03:FF:4F:1B:57:02:30 A1:A2:A3:A4:A5:A6:A7:A8 B1:B2:B3:B4:B5:B6:B7:B8
SQLSRV01A_Z2 A0:03:FF:4F:1B:57:02:31 A1:A2:A3:A4:A5:A6:A7:A8 B1:B2:B3:B4:B5:B6:B7:B8
SQLSRV01A_Z3 A0:03:FF:4F:1B:57:02:32 A1:A2:A3:A4:A5:A6:A7:A8 B1:B2:B3:B4:B5:B6:B7:B8
SQLSRV01A_Z4 A0:03:FF:4F:1B:57:02:33 A1:A2:A3:A4:A5:A6:A7:A8 B1:B2:B3:B4:B5:B6:B7:B8
SQLSERV02A_Z1 B0:03:FF:4F:1B:57:02:50 C1:C2:C3:C4:C5:C6:C7:C8 D1:D2:D3:D4:D5:D6:D7:D8
SQLSERV02A_Z2 B0:03:FF:4F:1B:57:02:51 C1:C2:C3:C4:C5:C6:C7:C8 D1:D2:D3:D4:D5:D6:D7:D8
SQLSERV02A_Z3 B0:03:FF:4F:1B:57:02:52 C1:C2:C3:C4:C5:C6:C7:C8 D1:D2:D3:D4:D5:D6:D7:D8
SQLSERV02A_Z4 B0:03:FF:4F:1B:57:02:53 C1:C2:C3:C4:C5:C6:C7:C8 D1:D2:D3:D4:D5:D6:D7:D8

out_zones.txt
zone name SQLSRV01A_Z1 vsan 2
	member pwwn A1:A2:A3:A4:A5:A6:A7:A8
	member pwwn B1:B2:B3:B4:B5:B6:B7:B8
	member pwwn A0:03:FF:4F:1B:57:02:30
zone name SQLSRV01A_Z2 vsan 2
	member pwwn A1:A2:A3:A4:A5:A6:A7:A8
	member pwwn B1:B2:B3:B4:B5:B6:B7:B8
	member pwwn A0:03:FF:4F:1B:57:02:31
zone name SQLSRV01A_Z3 vsan 2
	member pwwn A1:A2:A3:A4:A5:A6:A7:A8
	member pwwn B1:B2:B3:B4:B5:B6:B7:B8
	member pwwn A0:03:FF:4F:1B:57:02:32
zone name SQLSRV01A_Z4 vsan 2
	member pwwn A1:A2:A3:A4:A5:A6:A7:A8
	member pwwn B1:B2:B3:B4:B5:B6:B7:B8
	member pwwn A0:03:FF:4F:1B:57:02:33
zone name SQLSERV02A_Z1 vsan 2
	member pwwn C1:C2:C3:C4:C5:C6:C7:C8
	member pwwn D1:D2:D3:D4:D5:D6:D7:D8
	member pwwn B0:03:FF:4F:1B:57:02:50
zone name SQLSERV02A_Z2 vsan 2
	member pwwn C1:C2:C3:C4:C5:C6:C7:C8
	member pwwn D1:D2:D3:D4:D5:D6:D7:D8
	member pwwn B0:03:FF:4F:1B:57:02:51
zone name SQLSERV02A_Z3 vsan 2
	member pwwn C1:C2:C3:C4:C5:C6:C7:C8
	member pwwn D1:D2:D3:D4:D5:D6:D7:D8
	member pwwn B0:03:FF:4F:1B:57:02:52
zone name SQLSERV02A_Z4 vsan 2
	member pwwn C1:C2:C3:C4:C5:C6:C7:C8
	member pwwn D1:D2:D3:D4:D5:D6:D7:D8
	member pwwn B0:03:FF:4F:1B:57:02:53

out_zoneset.txt
member SQLSRV01A_Z1
member SQLSRV01A_Z2
member SQLSRV01A_Z3
member SQLSRV01A_Z4
member SQLSERV02A_Z1
member SQLSERV02A_Z2
member SQLSERV02A_Z3
member SQLSERV02A_Z4
'''

__author__ = 'mmussin'

import os
import re
import sys

class Pwwn(str):
    ' World-wide number port for fiber channel, formats any string to xx:xx:xx:xx:xx:xx:xx form '

    def isValidHex(self, pwwnStr):
        # Verifies if string is HEX
        if re.match(r'^([A-Fa-f0-9]{2}){8,9}$', pwwnStr):
            return True
        else:
            return False

    def replaceDelimiters(self, string, delimiter = ''):
        # Substitutes any separator character except underscore with colon, e.g. C0.03 FF;23-24!8F=00,60 to C0:03:FF:23:24:8F:00:60
         return re.sub(r'\W', delimiter, string)

    def splitToAddress(self, string, delimiter = ':', i = 1):
        # Continuous string is split by colon, e.g. 500a098689fb41f8 to 50:0a:09:86:89:fb:41:f8
        string_t = string[:1]
        for i in range(i, len(string), 2):
            string_t += delimiter.join(string[i:i+2])
        return string_t

    def preparePwwn(self, string):
        # Formats input string to match PWWN format
        pwwn = self.replaceDelimiters(string)
        if self.isValidHex(pwwn):
            return self.splitToAddress(pwwn)
        else:
            return string

class Zone():
    ' FC Zone class'
    __doc__ = ' Class structure that holds information about FC zone'

    zone = {'server_name'   : '',
            'port_init'     : '',
            'port_target_1' : '',
            'port_target_2' : ''}

    def writeZone(self):
        return ('\nzone name %s vsan 2\n\tmember pwwn %s\n\tmember pwwn %s\n\tmember pwwn %s' %
               (self.zone['server_name'] , self.zone['port_target_1'] , self.zone['port_target_2'] , self.zone['port_init']))

    def writeZoneset(self):
        return ('member %s\n' % self.zone['server_name'])

    def prepareZone(self, name, init, target1, target2):
        self.zone['server_name'] = name
        self.zone['port_init'] = init
        self.zone['port_target_1'] = target1.replace(' ','')
        self.zone['port_target_2'] = target2.replace(' ','')

if __name__ == '__main__':
    # Iterate through the block of four lines that represents single server with four HBAs in following format:
    try:
        f_in = open(sys.argv[1], 'r')
        f_out = open(sys.argv[2], 'w')
        f_out_z = open(sys.argv[3], 'w')
        f_out_zset = open(sys.argv[4], 'w')
    except IOError:
        sys.exit('The file does not exist')

    # Remove all empty lines
    file_list = [line for line in f_in.read().split('\n') if line.strip()]
    fczone = Zone()
    pwwn = Pwwn()
    i = 0
    srv_name_buff = ''
    srv_name_appendix = 1

    for elem in file_list:
        l = elem.split()
        # First line with server name SERV1A    C3:FF:FF:1F:1B:51:0A:00	    A0:01:00:A0:C1:B2:01:A0    B0:01:00:A0:C1:B2:01:B0
        if len(l) == 4:
            srv_name_buff = l[0]
            srv_name_appendix = 1
            # Here is another output method that can be used: str.format()
            # l[0] = '%s_Z%s' % (srv_name_buff, str(srv_name_appendix))
            l[0] = '{0}_Z{1}'.format(srv_name_buff, str(srv_name_appendix))
            for k in range(1,4):
                l[k] = pwwn.preparePwwn(l[k])
        else:
            # Three remaining lines without server name field
            if len(l) == 3:
                srv_name_appendix += 1
                l.insert(0,'%s_Z%s' % (srv_name_buff, str(srv_name_appendix)))
                for k in range(1,4):
                    l[k] = pwwn.preparePwwn(l[k])
        print l

        f_out.write(' '.join(l) + '\n')
        fczone.prepareZone(l[0], l[1], l[2], l[3])
        f_out_z.write(fczone.writeZone())
        f_out_zset.write(fczone.writeZoneset())
        i += 1
