# Filename-change-detector
Detects change in filename and outputs the time of change
Here is a clean, professional README.md tailored for your script. It explains what the script does, how it works, and how to set it up.
File Timestamp & Tamper Catcher

A lightweight Python utility designed for Windows environments to extract accurate file system timestamps (Creation, Modification, and Access times) and monitor directory changes. This tool is particularly useful for digital forensics, file auditing, and detecting basic timestamp manipulation (timestomping) flags.
🚀 Features

    Metadata Extraction: Retrieves low-level file timestamps (Creation, Modification, and Access times) utilizing the Windows API.

    Tamper Red-Flags: Incorporates a foundation for tracking live file system modifications and identifying anomalies (such as a Creation time predating a Modification time).

    Timezone Correction: Automatically adjusts UTC timestamps to local time (configured for UTC+5:30).

🛠️ How It Works

The script bypasses standard Python os.stat limitations by leveraging pywin32 to interact directly with the Windows Kernel:

    Opens a file handle using win32con.FILE_FLAG_BACKUP_SEMANTICS (allowing it to open directories as well as files).

    Utilizes win32file.GetFileTime to fetch precise MAC (Modified, Accessed, Created) times.

    Sets up a ReadDirectoryChangesW buffer to catch real-time file name notifications.

📋 Prerequisites

This script requires Windows and Python 3.x.
Dependencies

You need to install the Windows extensions for Python (pywin32):
Bash

pip install pywin32

🔧 Setup & Usage

    Clone or Download the Repository:
    Bash

    git clone https://github.com/yourusername/file-tamper-catcher.git
    cd file-tamper-catcher

    Configure the File Path:
    Open catcher.py and modify the file_path variable to point to the file or folder you want to inspect:
    Python

    file_path = r"C:\Users\YourUsername\Desktop\TargetFileOrFolder"

    Run the Script:
    Bash

    python catcher.py

📝 Code Structure Overview

    get_actual_change_time(filepath): Core function that handles the Windows API file locking, metadata retrieval, and buffer reading.

    duration: A timedelta object used to shift the standard UTC output from Windows into your local timezone.

⚠️ Important Considerations

    Blocking Behavior: The current implementation of win32file.ReadDirectoryChangesW is a blocking call. If no changes happen in the directory while it executes, it will wait. For live asynchronous production monitoring, this would typically be moved to a background thread.

    Permissions: Depending on the target directory (e.g., C:\Windows or system root folders), you may need to run your terminal as an Administrator.
