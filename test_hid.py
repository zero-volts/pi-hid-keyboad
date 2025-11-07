#!/usr/bin/env python3
NULL_CHAR = chr(0)


# Enter: 0x28
# Spacebar: 0x2C
# Left Shift: 0xE1
MOD_LEFT_SHIFT = 0xE1
ALPHABET = {
    'a': 0x04, 'b': 0x05, 'c': 0x06, 'd': 0x07, 'e': 0x08,
    'f': 0x09, 'g': 0x0A, 'h': 0x0B, 'i': 0x0C, 'j': 0x0D,
    'k': 0x0E, 'l': 0x0F, 'm': 0x10, 'n': 0x11, 'o': 0x12,
    'p': 0x13, 'q': 0x14, 'r': 0x15, 's': 0x16, 't': 0x17,
    'u': 0x18, 'v': 0x19, 'w': 0x1A, 'x': 0x1B, 'y': 0x1C,
    'z': 0x1D,
    ' ': 0x2C
}

def write_report(report):
 #   print("report: ", report)
#    print("report size", len(report) )
    with open('/dev/hidg0', 'wb') as fd:
        fd.write(report)
    

def send_message(message):
    for char in message:
        #report_array = [chr(0x0), chr(0x0), chr(ALPHABET[char]), chr(0x0), chr(0x0), chr(0x0), chr(0x0), chr(0x0)]
        report_array = bytearray([MOD_LEFT_SHIFT, 0x0, ALPHABET[char], 0x0, 0x0, 0x0, 0x0, 0x0])
        write_report(report_array)
        #write_report(bytearray([0x0, 0x0, 0x0, 0x0, 0x0, 0x0,0x0,0x0])) # release key

# # Press a
#write_report(NULL_CHAR*2+chr(0x1D)+NULL_CHAR*5)
# write_report(NULL_CHAR*2+chr(0x08)+NULL_CHAR*5)
# write_report(NULL_CHAR*2+chr(0x15)+NULL_CHAR*5)
# write_report(NULL_CHAR*2+chr(0x12)+NULL_CHAR*5)

send_message("hola")
