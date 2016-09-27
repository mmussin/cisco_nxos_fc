# cisco_nxos_fc

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
