Dropbox Ignore
==============
Python scripts for managing Dropbox selective sync.

dropbox_ignore
--------------
Make Dropbox ignore all folders that match a name pattern.
You can change the match pattern by modifying the 'ignoreList' variable.

The ignored folders will be deleted from Dropbox (thus freeing up Dropbox space). The local content of the folder will be deleted i.e. ignored folder on your computer will be emptied. However, any content added to the ignored folders after that will no longer by synced to Dropbox.
NOTE: if you have several machines linked to your Dropbox account 'dropbox_ignore' has to be run on all machines to make sure that the ignored folder is not uploaded to Dropbox.

*Usage*: dropbox_ignore <folder_path> [parameters]
By default the script does not execute any ignore operations. Use '-e' parameter to execute.

*Parameters*:
* -h:    show this message
* -e:    execute the operation
* -v:    print folders that are already ignored

*How it works:*
This script executes the following steps:
1. Delete local folder. This will also delete folder it from Dropbox account.
2. Add folder name to Selective Sync.
3. Create a new empty local folder with the same name.

**WARNING!!!**
Executing this script will delete both local and remote content for the folders which match the naming pattern. Locally deleted files will not go to Trash. Make sure you understand how this script works before your run it. Use at your own risk!
