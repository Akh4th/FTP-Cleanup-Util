## FTP-Cleanup-Util
A Python script to cleanup a server using an FTP connection

# Usage
1. Configure FTP Credentials: Set your FTP server's hostname, port, username, and password in the script.
2. Run the Script: Execute the script. It will first clear the 'tmp' directory, then proceed to delete unnecessary files and directories.
3. Monitor Output: Watch the console output for progress updates and actions taken.

# Features
○ Targeted File Deletion: Automatically deletes files with extensions like .txt, .zip, .gzip.
○ Directory Cleaning: Clears contents of directories named 'backup' and 'tmp', while keeping 'tmp' directory intact.
○ Recursive Search: Navigates through the server's file structure to ensure comprehensive cleanup.
○ Robust Error Handling: Includes reconnection logic for handling network interruptions and server timeouts.
○ User Feedback: Provides console output for monitoring script actions and progress.
○ Customization: Allows users to modify targeted file extensions and directory names as needed.

# Requirements 
• Python 3.x (Tested on 3.8 and above)
• Stable internet connection
• Sufficient permissions on the FTP server for file and directory operations

# Safety 
• Test the script in a controlled environment before deploying on a production server.
• Ensure backup of important data before running the script.
