from ctypes.wintypes import *
from ctypes import *

import ctypes

# Includes all processes in the snapshot.
_TH32CS_SNAPPROCESS = 0x00000002


class PROCESSENTRY32(Structure):
    """Entry from a list of processes when snapshot was taken.
    
    More info: https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/ns-tlhelp32-processentry32
    """
    _fields_ = [
        ( 'dwSize' , DWORD ),
        ( 'cntUsage' , DWORD),
        ( 'th32ProcessID' , DWORD),
        ( 'th32DefaultHeapID', POINTER(ULONG)),
        ( 'th32ModuleID' , DWORD),
        ( 'cntThreads' , DWORD),
        ( 'th32ParentProcessID' , DWORD),
        ( 'pcPriClassBase' , LONG),
        ( 'dwFlags' , DWORD),
        ( 'szExeFile' , c_char * 260 ),
    ]

def GetModulePIDs(module_name: str) -> list[int]:
    """Obtains the PIDs associated with the given module.
    
    Args:
        module_name: The name of the searched module, e.g. notepad.exe.
    Returns:
        Associated PIDs or an empty list.
    """

    pids = []
    entry = PROCESSENTRY32()
    # Set the size of structure before use it
    entry.dwSize = sizeof(entry)
    
    # Take snapshot of all processes
    snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot(_TH32CS_SNAPPROCESS, 0)
    
    # Retrive informations about first process,
    # and skip if unsuccessful
    if ctypes.windll.kernel32.Process32First(snapshot, byref(entry)):
        # Walk the snapshot of processes
        while ctypes.windll.kernel32.Process32Next(snapshot, byref(entry)):
            # If the module name matches, add pid to the list
            if entry.szExeFile.decode('utf-8') == module_name:
                pids.append(entry.th32ProcessID)
    
    # Clear the snapshot object.
    ctypes.windll.kernel32.CloseHandle(snapshot)
    
    return pids