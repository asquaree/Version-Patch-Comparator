usage = '''

Patch Comparator CLI.

Usage:
    diff_patch_driver.py clone_repository <repository_link> 
    diff_patch_driver.py compare_versions <repository_link> <version1> <version2>
    diff_patch_driver.py compare_consecutive_versions <repository_link>
    diff_patch_driver.py compare_versions_patch <repository_link> <version1> <version2> <patch>

'''

from docopt import docopt
from consecutive_versions_patch_comparator import *

args = docopt(usage)
print(args)

if args['clone_repository']:
    repo_link= args['<repository_link>']
    clone_repo(repo_link)

if args['compare_consecutive_versions']:
    repo_link= args['<repository_link>']
    compare_consecutive_versions(repo_link)

if args['compare_versions']:
    repo_link= args['<repository_link>']
    ver1=args['<version1>']
    ver2=args['<version2>']
    compare_2_versions(repo_link,ver1,ver2)

if args['compare_versions_patch']:
    repo_link= args['<repository_link>']
    ver1=args['<version1>']
    ver2=args['<version2>']
    patch=args['<patch>']
    compare_2_patches(repo_link,ver1,ver2,patch)



