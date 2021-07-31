usage = '''

Patch Comparator CLI.

Usage:
    diff_patch_driver.py clone_repository <repository_link> 
    diff_patch_driver.py compare_branches <repository_link> <branch1> <branch2>
    diff_patch_driver.py compare_consecutive_branches <repository_link>
    diff_patch_driver.py compare_branches_patch <repository_link> <branch1> <branch2> <patch>

'''

from docopt import docopt
from consecutive_versions_patch_comparator import *

args = docopt(usage)
print(args)

if args['clone_repository']:
    repository_link= args['<repository_link>']
    clone_repository(repository_link)

if args['compare_consecutive_branches']:
    repo_link= args['<repository_link>']
    compare_consecutive_branches(repo_link)

if args['compare_branches']:
    repo_link= args['<repository_link>']
    ver1=args['<branch1>']
    ver2=args['<branch2>']
    compare_2_branches(repo_link,ver1,ver2)

if args['compare_branches_patch']:
    repo_link= args['<repository_link>']
    ver1=args['<branch1>']
    ver2=args['<branch2>']
    patch=args['<patch>']
    compare_2_patches(repo_link,ver1,ver2,patch)



