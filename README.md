# get-PIDs-by-module-name-py

Python module that allows you to find process IDs by module name.
Code **works** only with **Windows** operating system.

## Depediences
The code does not need any additional dependencies.

## Example Usage
Find all processes related to the module and perform operations on them.
```python
# You need to install the pywin32 package to import these two packages
import win32api
import win32con

pids = GetModulePIDs('notepad.exe') # Get pids of notepad.exe

for pid in pids:
    # Obtain a handle for process with all access
    handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, 0, pid)
    
    # ...

    # Clean handle
    win32api.CloseHandle(handle)
```
