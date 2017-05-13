#!/usr/bin/python

import subprocess
import os
import shutil
import sys
from time import sleep

################################################################################
# Print usage
################################################################################
def printUsage(argv0):

  [curDir, scriptFilename] = os.path.split(argv0)

  print "Make Dropbox ignore all folders that match a name pattern."
  print "You can change the match pattern by modifying the 'ignoreList' variable."
  print
  print "The ignored folders will be deleted from Dropbox (thus freeing up Dropbox space). \
The local content of the folder will be deleted i.e. ignored folder on your \
computer will be emptied. However, any content added to the ignored folders \
after that will no longer by synced to Dropbox."
  print ""
  print "This script executes the following steps:"
  print "  1. Delete local folder. This will also delete folder it from Dropbox account."
  print "  2. Add folder name to Selective Sync."
  print "  3. Create a new empty local folder with the same name."
  print ""
  print "NOTE: if you have several machines linked to your Dropbox account \
" + scriptFilename + " has to be run on all machines to make sure that the ignored folder \
is not uploaded to Dropbox."
  print ""
  print "Usage: " + scriptFilename + " <folder_path> [parameters]"
  print "By default the script does not execute any ignore operations. Use '-e' \
  parameter to execute."
  print
  print "Parameters:"
  print "    -h:    show this message"
  print "    -e:    execute the operation"
  print "    -v:    print folders that are already ignored"
  print ""
  print "----------"
  print "WARNING!!!"
  print "----------"
  print "  Executing this script will delete both local and remote content for \
the folders which match the naming pattern. Locally deleted files will not go to Trash. \
Make sure you understand how this script works before your run it. Use at your own risk!"

################################################################################
# Parse command line
################################################################################

def parseCommandLine(argv):

  # Find help flag
  for arg in argv:
    if arg == "-h" or arg == "--help":
      printUsage(argv[0])
      sys.exit()

  # Find test and directory flags
  execute = False
  verbose = False
  targetDir = "."

  numArguments = min(len(argv), 4)
  for argId in range(1, numArguments):
    arg = argv[argId]
    if arg == "-e":
      execute = True
    elif arg == "-v":
      verbose = True
    else:
      targetDir = arg

  return targetDir, execute, verbose

################################################################################
# Main
################################################################################
# The script does the following:
#
#   * Find addFolders - folders that match description, exist on local HDD and
#     are not in the exclude list
#   * For folder in addFolders
#     - remove folder from local HDD
#     - add folder to the exclude list
#     - create an empty folder with same name at the same location
#
################################################################################

def main(argv):

  ignoreList = ["build", "bin", "lib"];

  print

  # Get current directory and script name
  [curDir, scriptName] = os.path.split(argv[0])

  # Parse command line
  [targetDir, execute, verbose] = parseCommandLine(argv)

  # Check that target directory exists
  if not os.path.isdir(targetDir):
    print "'" + targetDir + "' is not a directory or does not exist."
    sys.exit()

  print "----------------------------------------------------------------------"  
  print "Ignoring folders in '" + targetDir + "'"

  if verbose:
    print "Ignoring folders that match: "
    for pattern in ignoreList:
      print "  " + pattern

  #-----------------------------------------------------------------------------
  # Get all folders that are already excluded
  #-----------------------------------------------------------------------------
  alreadyExcluded = []

  p = subprocess.Popen(["dropbox", "exclude", "list"],
                       stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT)
  stdout = iter(p.stdout.readline, b'')

  for line in stdout:
    item = line[:-1]
    item = os.path.relpath(item)
    alreadyExcluded.append(item)

  alreadyExcluded = alreadyExcluded[1:]

  print
  print "----------------------------------------------------------------------"
  print "Already ignored: " + str(len(alreadyExcluded)) + " folders"

  if verbose:
    print
    if len(alreadyExcluded) == 0:
      print "  None"
    else:
      for item in alreadyExcluded:
        print "  " + item

  #-----------------------------------------------------------------------------
  # Get all folders that need to be excluded
  #-----------------------------------------------------------------------------
  shouldBeExcluded = []

  for root, dirnames, filenames in os.walk(targetDir):
    k = root.rfind("/")    
    if root[k+1:] in ignoreList:
      if root[0:2] == "./":
        root = root[2:]
      shouldBeExcluded.append(os.path.relpath(root))

  print
  print "----------------------------------------------------------------------"
  print "Should be ignored: " + str(len(shouldBeExcluded)) + " folders"

  if verbose:
    print
    if len(shouldBeExcluded) == 0:
      print "  None"
    else:  
      for item in shouldBeExcluded:
        print "  " + item

  #-----------------------------------------------------------------------------  
  # Get a list of folders that need to be added to excludes
  #-----------------------------------------------------------------------------
  addToExclude = [item for item in shouldBeExcluded if item not in alreadyExcluded]

  print
  print "----------------------------------------------------------------------"
  print "Should be added to the ignored list: " + str(len(addToExclude)) + " folders"

  print
  if len(addToExclude) == 0:
    print "  None"
  else:  
    for item in addToExclude:
      print "  " + item

  #-----------------------------------------------------------------------------
  # Set folders to ignore
  #-----------------------------------------------------------------------------

  # If not execute
  if not execute:
    print
    print "----------------------------------------------------------------------"
    print "NO changes were made. To add propsed folders to Dropbox ignore list run this \
with '-e' flag."
    return

  # Execute
  print
  print "----------------------------------------------------------------------"
  print "WARNING: this will delete folders from your computer. Make sure you understand \
  what this script does before continuing."
  print "Are you sure you want to continue? [y/n]"

  choice = raw_input().lower()

  if not (choice == 'y'):
    print "You choose to abandon the changes."
    return

  else:
    for folder in addToExclude:

      # Delete folder
      shutil.rmtree(folder)

      # Wait for a bit for dropbox website to receive changes
      sleep(5.0)

      # Wait till folder is deleted
      while os.path.exists(folder):
        pass  # do nothing

      # Exclude folder
      p = subprocess.Popen(["dropbox", "exclude", "add", folder],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
      stdout = iter(p.stdout.readline, b'')

      print
      for line in stdout:
        print line[:-1]

      # Recreate folder
      os.mkdir(folder)

################################################################################
# Entry
################################################################################
if __name__ == "__main__":
  main(sys.argv)  