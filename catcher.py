import win32file
import win32con
from datetime import datetime,timedelta
from tqdm.contrib.concurrent import thread_map
import subprocess

duration = timedelta(hours=5, minutes=30)


def disable_adapter(adapter_name):
    try:
        # Command to disable the specified network adapter
        cmd = f'netsh interface set interface "{adapter_name}" disable'
        subprocess.run(cmd, shell=False, check=True)
        print(f"Successfully disabled {adapter_name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to disable adapter. Error: {e}")

def check_malware(filepath):
    handle = win32file.CreateFile(
        filepath,
        win32con.GENERIC_READ,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_FLAG_BACKUP_SEMANTICS,
        None
    )
    i=0
    already_counted_files = set()

    while True:        
        results = win32file.ReadDirectoryChangesW(handle, 60000, True, win32con.FILE_NOTIFY_CHANGE_FILE_NAME)
        
        current_time = datetime.now()
        new_files_detected = False
                
        for action, file_name in results:
            # Ignore temporary files editors create
            if file_name.endswith('.tmp') or file_name.startswith('~'):
                continue
                
            if file_name not in already_counted_files:
                if i == 0:
                    start_time = current_time
                
                already_counted_files.add(file_name)
                i += 1 
                new_files_detected = True
                print(f"[{current_time.strftime('%H:%M:%S')}] Distinct File Targeted: {file_name} (Total distinct: {i})")
        
            elapsed_time = current_time - start_time

        if i > 10 and elapsed_time <= timedelta(seconds=5):
            print(f"Ransomware behavior detected")
            print(f"{i} distinct files altered in {elapsed_time.total_seconds()} seconds")
            disable_adapter("WiFi")
            disable_adapter("Ethernet")
            break

        elif elapsed_time > timedelta(seconds=5):
            if new_files_detected:
                print(f"[Cool-down] Time window expired safely. Resetting session trackers.")
            i = 0
            start_time = None
            already_counted_files.clear()
                                            
# Usage
file_paths = [r"C:\Users\Admin\Desktop",r"C:\Users\Admin\Downloads",r"C:\Users\Admin\Documents",r"C:\Users\Admin\Picturs",r"C:\Users\Admin\Video"] #your path
thread_map(check_malware,file_paths,max_workers=5)