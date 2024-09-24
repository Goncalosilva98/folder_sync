
########  #######  ##       ########  ######## ########      ######  ##    ## ##    ##  ######  
##       ##     ## ##       ##     ## ##       ##     ##    ##    ##  ##  ##  ###   ## ##    ## 
##       ##     ## ##       ##     ## ##       ##     ##    ##         ####   ####  ## ##       
######   ##     ## ##       ##     ## ######   ########      ######     ##    ## ## ## ##       
##       ##     ## ##       ##     ## ##       ##   ##            ##    ##    ##  #### ##       
##       ##     ## ##       ##     ## ##       ##    ##     ##    ##    ##    ##   ### ##    ## 
##        #######  ######## ########  ######## ##     ##     ######     ##    ##    ##  ######  



Internal Development in QA (SDET) - Gonçalo Silva

The pythonm script performs one-way folder synchronization between two directories (source and replica)

The tool ensures that the replica directory mirrors the source directory, copying new files and updating modified ones from the source to the replica. Additionally, it removes files and directories from the replica that no longer exist in the source directory.


FEATURES:

1 - One-Way Synchronization:
    
    - Copies new files from the source directory to the replica directory.
    - Updates existing files in the replica if they have changed in the source.
    - Removes files and folders from the replica if they no longer exist in the source.

2 -  Hash-based file comparison:
    
    - File changes are detected using sha-256 hash comparison.

3 - Multi-threaded execution:

    - Synchronization operations are performed using ThreadPoolExecutor for faster processing.

4 - Logging:

    - Every operation is logged in the console output and the Log files and saved with time stamps.

5 - Periodic Execution:

    - The script automatically repeats the synnchronization process at a user-specified time interval (in seconds).




USAGE:

    Run the script using the following command:

    python file_sync.py <source_dir> <replica_dir> <interval>

    Arguments:

    - source_dir: The directory you want to sync from.
    - replica_dir: The target directory that will replicate the source (if it is not created yet, specify the path in wihch you wish for it to be created).
    - interval: Time interval (in seconds) between each synchronization cycle.





AUTHOR:

Developed by Gonçalo Silva. If you have any questions feel free to reach out!