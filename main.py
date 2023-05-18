import evdev
import time
from database import *
# Find the input device with the name "RFID reader"
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
rfid_device = None




def read():
    for device in devices:

        if device.name == 'BARCODE SCANNER Keyboard Interface':
            rfid_device = device
            break
    global data
    data = []

    global data
    # If the RFID reader was found, read from it
    if rfid_device is not None:
        if data == []:
            print('Found RFID reader:', rfid_device.name)
        global rfid_tag
        rfid_tag = ''
        for event in rfid_device.read_loop():
            if event.type == evdev.ecodes.EV_KEY and event.value == 1:
                digit = evdev.categorize(event).keycode
                if digit == "KEY_ENTER":
                    rfid_tag = str(rfid_tag)
                    datas = search_user(rfid_tag)

                    if datas == False:
                        print(f'RFID tag ({rfid_tag}) has been read.')
                        print("You don't have authorization ")
                        log_history(f"card: {rfid_tag}", "Authorization Error")
                        rfid_tag = ""
                        break

                    else:

                        print(
                            f"\nCard number: {rfid_tag}({datas[0]}) with Owner_name: {datas[1]}({datas[2]}), Rank:{datas[4]}-{datas[5]} and phone number: {datas[3]}. Has entered\n")
                        log_history(datas[2],
                                    f"Card number: {rfid_tag}({datas[0]}) with Owner_name: {datas[1]}({datas[2]}), Rank:{datas[4]}-{datas[5]} and phone number: {datas[3]}. Has entered")
                        rfid_tag = ""
                        break

                else:

                    if digit[-1].isdigit():
                        rfid_tag += digit[-1]
    else:
        print('RFID reader not found.')
        time.sleep(5)

while True:
    read()
    
   

    
