# pi-hid-keyboard
Configuracion para hacer que la raspberry pi 4 se comporte como un dispositivo HID tipo teclado al conectarlo a otro computador.
Funciona igual que un Rubber Ducky, permitiendo enviar pulsaciones de teclado automatizadas al host conectado por USB-C.

Nota: Todo estos pasos son hechos especialmente para aprender el funcionamiento de HID y creacion de servicios. Hay mejores formas de hacer esto, ira evolucionando en el tiempo

---

## 1. Habilitar controlador DWC2

1. Edita el archivo de configuración del sistema:
   ```bash
   sudo nano /boot/firmware/config.txt
   ```

2. Al final agregar la siguiente linea:
    ```ini
   doverlay=dwc2,dr_mode=peripheral
   ```

## 2. Habilitar libcomposite

Esto nos sirve para poder definir gadgets USB dentro del espacio de usuario.

1. Edita el archivo 
    ```bash
   sudo nano /boot/firmware/cmdline.txt
   ```

2. Al final sin espacios agregar:
    ```ini
   modules-load=dwc2,libcomposite
   ```

---

# Scripts

1. **zv-hid-setup.sh**

   El script crea en /sys/kernel/config/usb_gadget/ un dispositivo USB virtual "zerovolts-hid" 

2. **zv-hid.service**

   Ejecuta automaticamente el script para crear el gadget en el inicio. El servicio debe ser creado en:
    ```bash
   /etc/systemd/system/zv-hid.service
   ```

   El script "zv-hid-setup.sh" debe ser copiado en:
    ```bash
   /usr/local/bin/
   ```

   Dar permisos de ejecucion:
   ```bash
   sudo chmod +x zv-hid-setup.sh
   ```

3. **test_script.py**

   Script basico en python para probar el envio de teclas automatico
   
### Capitulos de youtube
-----
Videos con el proceso de configuración y programación 

1. [Configuracion y creacion de script](https://www.youtube.com/watch?v=WQ7kpHHoVA4)
2. [Correccion del descriptor y corriendo script de prueba](https://www.youtube.com/watch?v=kefJoc_F7kg)
3. [Inicializacion automatica con systemd](https://www.youtube.com/watch?v=AaPY0jVu0lY)
