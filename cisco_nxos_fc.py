'''
The program generates Cisco NX-OS Fiber Channel configuration that is ready to paste into NX-OS
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
