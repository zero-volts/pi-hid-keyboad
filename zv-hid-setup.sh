#!/usr/bin/env bash
# Script to create the HID keyboard using libcomposite
# Must be executed as root
# https://www.usb.org/sites/default/files/documents/hid1_11.pdf

GADGET_DIR=/sys/kernel/config/usb_gadget/zerovolts-usb
UDC_PATH="$GADGET_DIR/UDC" # files to bind/unbind to the UDC
REPORT_DESC_BIN=$GADGET_DIR/functions/hid.usb0/report_desc

# 1.- Mounting configfs if is not. (this allow to create gadgets)
if ! mountpoint -q /sys/kernel/config; then
  echo "[1/10] Mounting configfs in /sys/kernel/config..."
  mount -t configfs none /sys/kernel/config
else
  echo "[1/10] configfs already mounted."
fi

# 2.- Loading the libcomposite module
echo "[2/10] Loading libcomposite module ..."
if ! lsmod | grep -q '^libcomposite'; then
    modprobe libcomposite
else 
    echo "*** libcomposite already loaded"
fi

# 3.- Making the gadget directory (virtual object)
echo "[3/10] Making gadget directory: $GADGET_DIR"
if [ -d "$GADGET_DIR" ]; then
  echo "*** The gadget already exists"
else
  mkdir -p "$GADGET_DIR"
fi

cd "$GADGET_DIR"

# 4.- Defining the device identification.
echo "[4/10] Writing device identifications"
printf '0x1d6b' > idVendor      # Vendor id, (Linux Foundation)
printf '0x0104' > idProduct     # Product id, change this later
printf '0x0200' > bcdUSB        # USB 2.0
echo "*** idVendor: $(cat idVendor), idProduct: $(cat idProduct), bcdUSB: $(cat bcdUSB)"

# 5.- strings that hosts will see when the device is connected.
# The 0x409 = en-US
echo "[5/10] Writing device string configuration"
mkdir -p "$GADGET_DIR/strings/0x409"
printf 'Zerovolts'      > "$GADGET_DIR/strings/0x409/manufacturer"
printf 'zv-keyboard'    > "$GADGET_DIR/strings/0x409/product"
printf '00001'          > "$GADGET_DIR/strings/0x409/serialnumber"
echo "*** manufacturer: $(cat "$GADGET_DIR/strings/0x409/manufacturer")"

echo "[6/10] Gadget configurations"
mkdir -p "$GADGET_DIR/configs/c.1/strings/0x409"
printf 'Config : HID keyboard' > "$GADGET_DIR/configs/c.1/strings/0x409/configuration"
printf '120' > "$GADGET_DIR/configs/c.1/MaxPower"  # 120 mA

# protocol: 1 boot keyboad; subclass: 1 boot; report_length: 8 bytes
echo "[7/10] Making HID function hid.usb0 and parameters(protocol, subclass,report_length)"
mkdir -p "$GADGET_DIR/functions/hid.usb0"
printf '1' > "$GADGET_DIR/functions/hid.usb0/protocol"
printf '1' > "$GADGET_DIR/functions/hid.usb0/subclass"
printf '8' > "$GADGET_DIR/functions/hid.usb0/report_length"

echo "[8/10] Writing report_desc (HID descriptor)"
bash -c "cat > '$REPORT_DESC_BIN' <<'EOF'
\x05\x01\x09\x06\xa1\x01\x05\x07\x19\xe0\x29\xe7\x15\x00\x25\x01
\x75\x01\x95\x08\x81\x02\x95\x01\x75\x08\x81\x01\x95\x06\x75\x08
\x15\x00\x25\x65\x05\x07\x19\x00\x29\x65\x81\x00\xc0
EOF"

echo "[9/10] Linking the function to the configuration"
# checking configs/c.1 already exists before linking
if [ ! -d "$GADGET_DIR/configs/c.1" ]; then
    echo " ERROR $GADGET_DIR/configs/c.1 doesn't existes. Making it..."
    mkdir -p "$GADGET_DIR/configs/c.1/strings/0x409"
fi

ln -sf "$GADGET_DIR/functions/hid.usb0" "$GADGET_DIR/configs/c.1/hid.usb0"
ls -l "$GADGET_DIR/configs/c.1" | sed -n '1,5p'

echo "[10/10] Showing UDC available in the system"
ls /sys/class/udc || true

echo ""
echo "To bind manually replace <UDC_NAME> by 'ls /sys/class/udc' result" 
echo "*** sudo bash -c 'echo <UDC_NAME> > $UDC_PATH'"
echo "To unbind" 
echo "***  sudo bash -c 'echo \"\" > $UDC_PATH'"