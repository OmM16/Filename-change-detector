import win32file
import win32con
import os
from datetime import datetime, timedelta

duration = timedelta(hours=5, minutes=30)

def watch_tamper_stream(filepath):
    handle = win32file.CreateFile(
        filepath,
        win32con.GENERIC_READ,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_FLAG_BACKUP_SEMANTICS,
        None
    )

    ACTIONS = {
        1: "Created",
        2: "Deleted",
        3: "Modified/Tampered",
        4: "Renamed (Old Name)",
        5: "Renamed (New Name)"
    }

    try:
        while True:
            raw_results = win32file.ReadDirectoryChangesW(
                handle, 
                65536, 
                True, 
                win32con.FILE_NOTIFY_CHANGE_FILE_NAME | 
                win32con.FILE_NOTIFY_CHANGE_LAST_WRITE
            )
            
            tamper_history = []
            for action_id, filename in raw_results:
                action_name = ACTIONS.get(action_id, "Unknown Action")
                full_file_path = os.path.join(filepath, filename)
                
                # Default fallback timestamps if a file is deleted/missing
                f_created = "N/A (File Removed)"
                f_modified = "N/A (File Removed)"
                
                # If the file exists, open a quick read handle to grab its real metadata
                if os.path.exists(full_file_path):
                    try:
                        file_handle = win32file.CreateFile(
                            full_file_path,
                            win32con.GENERIC_READ,
                            win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE,
                            None,
                            win32con.OPEN_EXISTING,
                            0,
                            None
                        )
                        c_time, _, m_time = win32file.GetFileTime(file_handle)
                        file_handle.Close()
                        
                        f_created = str(c_time + duration)
                        f_modified = str(m_time + duration)
                    except Exception:
                        f_created = "Locked by OS"
                        f_modified = "Locked by OS"

                tamper_history.append({
                    "action": action_name, 
                    "file": filename,
                    "file_created": f_created,
                    "file_modified": f_modified
                })
            
            yield {
                "Tamper": tamper_history
            }
    finally:
        handle.Close()

if __name__ == "__main__":
    file_path = r"C:\Source\Projects\plc project\targets"
    print(f"[*] Security Monitor Active. Tracking: {file_path}\n")

    try:
        for times in watch_tamper_stream(file_path):
            log_time = datetime.now().strftime("%H:%M:%S")
            
            for event in times['Tamper']:
                print(f"[{log_time}] ALERT: File -> {event['file']} | Action -> {event['action']}")
                print(f"    --> Real File Created:  {event['file_created']}")
                print(f"    --> Real File Modified: {event['file_modified']}")
                print("-" * 50)
                
    except KeyboardInterrupt:
        print("\nMonitoring stopped manually.")