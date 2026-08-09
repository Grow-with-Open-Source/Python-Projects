import win32com.client
import wmi

def info_pc():
    c = wmi.WMI()    
    my_system = c.Win32_ComputerSystem()[0]

    print(f"Manufacturer: {my_system.Manufacturer}")
    print(f"Model: {my_system. Model}")
    print(f"Name: {my_system.Name}")
    print(f"NumberOfProcessors: {my_system.NumberOfProcessors}")
    print(f"SystemType: {my_system.SystemType}")
    print(f"SystemFamily: {my_system.SystemFamily}")


def list_plugged_in_devices():
    print("Loading getting machine devices\n")
    
    # WMI API
    wmi = win32com.client.GetObject("winmgmts:")

    # query used to get the device information
    devices = wmi.ExecQuery(
    """
     SELECT Name, DeviceID, Manufacturer, PNPClass, Present, ConfigManagerErrorCode 
        FROM Win32_PnPEntity 
        WHERE Present = True AND Manufacturer != 'Microsoft'
    """
    )

    
    print(f"({len(devices)} devices found: \n")
    for dev in list(devices):
        print(f"Device Name: {dev.Name}")
        print(f"  * Manufacturer: {dev.Manufacturer}")
        print(f"  * Class type:  {dev.PNPClass}")
        print(f"  * Device ID:  {dev.DeviceID}")
        print(f"  * Status Code:  {dev.ConfigManagerErrorCode} (0 = Working Perfect)")
        print("-" * 100)


def user_console():
    while True:
        print("\n See Pc information")
        print("1) Standard device information")
        print("2) Input devices")
        print("3) Quit")
        
        try:
            option = int(input("What would you like to see about your device? (1-3): "))
            
            if option == 1:
                info_pc()
            elif option == 2:
                list_plugged_in_devices()
            elif option == 3:
                print("Exiting console application. Goodbye!")
                break  
            else:
                print("Invalid choice! Please choose 1, 2, or 3.")
                
        except ValueError:
            print("Error: Please enter a valid number (1, 2, or 3).")

if __name__ == "__main__":
    user_console()
