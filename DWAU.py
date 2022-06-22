import os
import re
import sys
import enum
import ctypes
import subprocess 

class SW(enum.IntEnum):HIDE=0;MAXIMIZE=3;MINIMIZE=6;RESTORE=9;SHOW=5;SHOWDEFAULT=10;SHOWMAXIMIZED=3;SHOWMINIMIZED=2;SHOWMINNOACTIVE=7;SHOWNA=8;SHOWNOACTIVATE=4;SHOWNORMAL=1
class ERROR(enum.IntEnum):ZERO=0;FILE_NOT_FOUND=2;PATH_NOT_FOUND=3;BAD_FORMAT=11;ACCESS_DENIED=5;ASSOC_INCOMPLETE=27;DDE_BUSY=30;DDE_FAIL=29;DDE_TIMEOUT=28;DLL_NOT_FOUND=32;NO_ASSOC=31;OOM=8;SHARE=26

def bootstrap():
    if ctypes.windll.shell32.IsUserAnAdmin():
        main()
    else:
        hinstance = ctypes.windll.shell32.ShellExecuteW(
            None, 'runas', sys.executable, sys.argv[0], None, SW.SHOWNORMAL
        )
        if hinstance <= 32:
            raise RuntimeError(ERROR(hinstance))
def quit():
    print("Press enter to exit.")
    input()
def doesExist():
    try:
        cmd = 'reg query HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer /f "NoWindowsUpdate"'
        output = subprocess.check_output(cmd,).decode('utf-8')
        output = str(re.sub(r'b\'|\\r\\n|\'|\s|\n\t\s+','',output))
        test = "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\ExplorerNoWindowsUpdateREG_DWORD0x1Endofsearch:1match(es)found."
        if output == test:
            return True
        else:
            return False
    except:
        return False

def main():
    #os.system("cls")
    is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0    
    if is_admin == True:
        if doesExist() == False:
            os.system('reg add HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer /v "NoWindowsUpdate" /t REG_DWORD /d 1 /f')
            print("Windows Auto Updates Disabled!")
            quit()
        else:
            os.system('reg delete HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Policies\Explorer /v "NoWindowsUpdate" /f')
            print("Windows Auto Updates Re-enabled!")
            quit()
    else:
        print("not admin");
        quit()

if __name__ == '__main__':
    bootstrap()