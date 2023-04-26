from ppadb.client import Client as AdbClient
import argparse
import time

lockscreen_positions = {"1": (250, 1000), "2": (540, 1000), "3": (815, 1000), "4": (250, 1186), "5": (540, 1186), "6": (813, 1186),
                        "7": (250, 1390), "8": (540, 1390), "9": (813, 1390), "0":(538, 1590), "-1": (826, 1594), "OK": (186, 1367)}

def connect():

    client = AdbClient(host="127.0.0.1", port=5037) # Default is "127.0.0.1" and 5037

    devices = client.devices()

    if len(devices) == 0:
        print('No devices')
        quit()

    device = devices[0]

    print(f'Connected to {device}')

    return device, client

def try_pattern(device, pattern, method, seconds_to_wait):

    splitted_chars = list(pattern)

    if method == 'touch':
        for char in splitted_chars:
            position = lockscreen_positions[char]
            device.shell('input tap {} {}'.format(position[0], position[1]))

        if is_device_locked(device):
            if is_alert_dialog_displayed(device):

                position = lockscreen_positions['OK']
                device.shell('input tap {} {}'.format(position[0], position[1]))
                print("Detected locked screen and max tries. Sleeping 35 seconds...")
                time.sleep(seconds_to_wait)
            else:
                time.sleep(1)

            return False

        else:
            return True

    elif method == 'locksettings':
        ret = device.shell('locksettings verify --old {}'.format(pattern))

        if 'successfully' in ret:
            return True
        elif 'throttled' in ret:
            print("Detected max tries. Sleeping 35 seconds...")
            time.sleep(seconds_to_wait)

        return False


def is_device_locked(device):
    result = device.shell('dumpsys power | grep mHoldingDisplaySuspendBlocker=true')
    if result:
        return True
    return False

def is_alert_dialog_displayed(device):

    if device.shell('which uiautomator'):
        device.shell('uiautomator dump /sdcard/view.xml')
        if device.shell('cat /sdcard/view.xml | grep "Try again"'):
            return True

    return False

def generate_list(n_digits):

    n_list = []
    max_range = (10 ** n_digits) - 1

    for num in range(0, max_range):
        custom_str = '{0:0' + str(n_digits) + '}'
        n_list.append(custom_str.format(num))

    return n_list


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--ndigits", help="The number of PIN digits", required=False, type=int, default=4)
    parser.add_argument("-m", "--method", help="The method to use (touch or adb locksettings)", required=False, type=str, default='locksettings')
    parser.add_argument("-c", "--cooldown", help="Seconds to wait if a cooldown is detected", required=False, type=int, default=35)

    args = parser.parse_args()

    patterns = generate_list(args.ndigits)

    print("[!!!] You set the PIN as {} digits length. Please, take into account that if you have a cooldown of 35 "
          "seconds (the standard), it will last POSITION * 35 seconds to find the PIN.".format(args.ndigits))
    #print("- EXAMPLE: Your PIN is the #100 in the list this script will last 100*35= 3500 secs = 0.97h + execution time"
    #      "\nIf your PIN is the #500, the script will last 500*35= 17500 secs = 4.86h + execution time")
    print("- NOTE: 4 digits PIN could be up to 9999: The 10000th position: Up to 4,05 days. "
          "6 digits PIN could last 1,1 years ;)")

    device, client = connect()

    for pattern in patterns:

        print("Tying pattern {}".format(pattern))
        if try_pattern(device, pattern, args.method, args.cooldown):
            print("Found pattern! PIN: {}".format(pattern))
            exit()

    print("No pattern found. Sorry :'(")

