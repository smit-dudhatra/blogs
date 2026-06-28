Total size of a specific folder:

du -sh /path/to/folder

Sizes of all subdirectories (1st level deep):

du -h --max-depth=1 /path/to/folder

Count only subfolders inside a directory (excluding the directory itself)

find /path/to/folder -mindepth 1 -type d | wc -l


