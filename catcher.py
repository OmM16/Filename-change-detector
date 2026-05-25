import win32file
import win32con
from datetime import datetime,timedelta
duration = timedelta(hours=5, minutes=30)

def get_actual_change_time(filepath):
    
    #defining handle for reading the directory    
    handle = win32file.CreateFile(
        filepath,
        win32con.GENERIC_READ,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_FLAG_BACKUP_SEMANTICS,
        None
    )

    #reading info
    results = win32file.ReadDirectoryChangesW(handle, 60000, True, win32con.FILE_NOTIFY_CHANGE_FILE_NAME)
    create_time, access_time, write_time = win32file.GetFileTime(handle)
    
    handle.Close()
    
    return {
        "Created": create_time,
        "Modified": write_time,
        "Accessed": access_time,
        "Tamper": results
    }

# Usage
file_path = r"C:\Users\Admin\Documents" #your path
times = get_actual_change_time(file_path)
print(f"File Created: {times['Created'] + duration}")
print(f"File Modified: {times['Modified'] + duration}")
print(f"File Tampered: {times['Tamper'][0][1]} changed to {times['Tamper'][1][1]}")
