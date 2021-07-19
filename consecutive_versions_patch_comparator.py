# -*- coding: utf-8 -*-
"""Consecutive_versions_patch_comparator.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Q7c4Nli6ig76HUNmeZaWARdSgIcyFjXk

The main motive of this code is to:


1.   Clone the repository given to the local machine.
2.   Fetch all the branches from the cloned repository and store them into different folders named as For eg. F10.Where F10 folder contains all its patches.
3. Create text files for each consecutive versions where number of text files will be equal to (Number of patch files in F10)union(Number of patch files in F11).Each and every text file will contain diff in between PatchA of version1 and PatchA of version2.We will store all these diff text files in one folder named For eg.F10F11 F11F12 etc.
4.This is how we will be able to get N-1 folders(where N is no. of versions) consisting of diff files 
5.We will use these diff text files for futher analysis
"""
""""
pip install gitpython
pip install diff-match-patch
pip install numpy
pip install shutil
pip install os
pip install difflib
pip install diff_match_patch
pip install subprocess
pip install csv
"""




"""Importing libraries"""

import numpy as np
from git import Repo
import os
import shutil
import difflib
import diff_match_patch as diff_match_patch
import subprocess
import csv

# from google.colab import drive
# drive.mount('/content/drive')

"""Cloning the repository(NOT REQUIRED)

"""

# my_repo=Repo.clone_from("https://src.fedoraproject.org/rpms/grub2.git", "/content/Fedora project/repos")
# print(my_repo)

"""To delete a non empty folder"""

#shutil.rmtree(os.getcwd()+'\\'+'Fedora project')

"""Function to add empty patch file"""

def add_emptyfile(path,branch):
  file = 'emptyfile'+branch+'.patch'
  with open(os.path.join(path, file), 'w') as fp:
    pass

"""Cloning single single branch"""

def clone_version(all_version,repository_name):
    print('Cloning versions........')
    for i in range(len(all_version)):
      brch=all_version[i]
      path= os.getcwd()+'\\Fedora project'+'\\versions\\'+brch
      # print(brch)
      #print(path)
      Repo.clone_from(repository_name,path , branch=brch)
      add_emptyfile(path,brch)#adds an empty patch file in the folder

"""Finding version names"""

#  for i in range(10,35):
#    brch='f'+str(i)
#    path= "/content/Fedora project/versions/"+brch
#   # print(brch)
#    #print(path)
#    Repo.clone_from("https://src.fedoraproject.org/rpms/grub2.git",path , branch=brch)
#    add_emptyfile(path,brch)#adds an empty patch file in the folder

parent_dir=os.getcwd()
os.mkdir(os.path.join(parent_dir,'Fedora project'))
folder_name="versions"
parent_dir=parent_dir+'\\'+'Fedora project'
if not os.path.exists(parent_dir+folder_name):
  os.mkdir(os.path.join(parent_dir,folder_name))
#parent_dir+=folder_name+'/'

all_branches=[]

repository_name=input('Enter the repository git link:')
repository_name=str(repository_name)
subprocess.run(['git', 'clone',repository_name],cwd=parent_dir )
# subprocess.run(['cd',repository_name], stdout=True,text=True,stderr=subprocess.DEVNULL)
#all_versions = subprocess.check_output(['git', 'branch', '-a'],text=True,stderr=subprocess.DEVNULL,cwd=parent_dir+'/grub2').decode().split('\n')
#print[all_versions]
# print(all_versions.stdout)
stdout = subprocess.check_output('git branch -r'.split(),cwd=parent_dir+'\\grub2',)
out = stdout.decode()
all_branches = [b.strip('* ') for b in out.splitlines()]
#print(all_branches)
all_branches.sort()
all_version=[]
for i in range(len(all_branches)):
   branch_name='';
   all_branches[i]=all_branches[i][::-1]
   j=0;
   while(all_branches[i][j]!='/'):
     branch_name+=all_branches[i][j]
     j+=1;
   branch_name=branch_name[::-1]
   if(branch_name[0]=='f'):
     all_version.append(branch_name)
print('Version:\n')
print(all_version)
all_version.sort()
clone_version(all_version,repository_name)

"""function to find diff between 2 files"""

# def find_diff(file1,file2):
#   f1=open(file1,'r')
#   f2=open(file2,'r')
#   #Find and print the diff:
#   for line in difflib.unified_diff(f1, f2, fromfile='file1', tofile='file2'):
#     print(line)

def find_diff(file1,file2,diff_dir_path,file):
    PIPE = subprocess.PIPE
    branch1=file1
    branch2=file2
    with open(os.path.join(diff_dir_path, file),'w') as f:
      process = subprocess.run(['git', 'diff', branch1,branch2], stdout=f,text=True,stderr=subprocess.DEVNULL)
      #print(process.stdout)
    #stdoutput, stderroutput = process.communicate()

    # if 'fatal' in stdoutput:
    #   # Handle error case
    #   pass
    # else:
    #   # Success!
    #   pass

"""Function to compare 2 versions"""

def compare(version1,version2):
  diff_dir_name=""+version1+version2
  folder_name="versions_diff"
  diff_dir_parent_dir=os.getcwd()+"\\Fedora project\\"
  if not os.path.exists(diff_dir_parent_dir+folder_name):
    os.mkdir(os.path.join(diff_dir_parent_dir,folder_name))
  diff_dir_parent_dir+=folder_name+'\\'
  diff_dir_path = os.path.join(diff_dir_parent_dir, diff_dir_name)
  os.mkdir(diff_dir_path)

  path1=os.getcwd()+"\\Fedora project\\versions\\"+version1
  path2=os.getcwd()+"\\Fedora project\\versions\\"+version2
  version1_patch_files={}
  for file in os.listdir(path1):
    if file.endswith(".patch"):
        version1_patch_files[file]=1
  #print(version1_patch_files)
  for file in os.listdir(path2):
    if file.endswith(".patch"):
      print(file)
      if file in version1_patch_files.keys():
        version1_patch_files[file]=2
        version1_file=path1+"\\"+file
        version2_file=path2+"\\"+file
        find_diff(version1_file,version2_file,diff_dir_path,str(file))
        
      else:
        version2_file=path2+"\\"+file
        version1_file=path1+"\\"+'emptyfile'+version1+'.patch'
        find_diff(version1_file,version2_file,diff_dir_path,str(file))
  for file in version1_patch_files.keys():
    if version1_patch_files[file]==1:
      version2_file=path2+"\\"+'emptyfile'+version2+'.patch'
      version1_file=path1+"\\"+file
      find_diff(version1_file,version2_file,diff_dir_path,str(file))



"""Comparing branches"""

branches = os.listdir(os.getcwd()+'\\Fedora project\\versions')
branches.sort()
#print(branches[2])
for i in range(len(branches)-1):
  compare(branches[i],branches[i+1])

"""Function count_changes:

Creating csv file
"""

fields=['path_file','branch1','branch2','added_lines','deleted_lines','is_deleted']

csv_name="comparison_sheet.csv"
with open(os.path.join(os.getcwd()+'\\Fedora project',csv_name), 'w') as csvfile:
  csvwriter = csv.writer(csvfile) 
  csvwriter.writerow(fields)

"""function to count added deleted and number of lines in diff file"""

def count_lines(diff,path):
  added_lines=0
  deleted_lines=0
  total_lines=0
  infile = open(os.path.join(path,diff), 'r', encoding='mac_roman')
  text = infile.readlines()
  for j in (text):
    if(j[0]=='+'):
      added_lines+=1
    elif(j[0]=='-'):
      deleted_lines+=1
    total_lines+=1
  return added_lines,deleted_lines,total_lines;

"""Function to check changes in diff files of a folder"""

def check_changes(branch_diff):
  path=os.getcwd()+'\\Fedora project\\versions_diff'+'\\'+branch_diff
  for diff in os.listdir(path):
    patch_name=str(diff)
    print(patch_name)
    brch_diff=str(branch_diff)
    brch_diff_len=len(brch_diff)/2
   # print(brch_diff_len)
    #print(brch_diff)
    branch1=brch_diff[0:int(brch_diff_len)]
    branch2=brch_diff[int(brch_diff_len):]
    #print(branch1)
    #print(branch2)
    added_lines,deleted_lines,total_lines=count_lines(diff,path)
    print(added_lines)
    print(deleted_lines)
    print(total_lines)
    isdeleted=0
    if(deleted_lines!=0 and added_lines<=1):
      isdeleted=1
    with open(os.path.join(os.getcwd()+'\\Fedora project',csv_name), 'a') as csvfile:
      csvwriter = csv.writer(csvfile)
      csvwriter.writerow([patch_name,branch1,branch2,added_lines,deleted_lines,isdeleted])

"""Fetching each diff folder"""

diff_folders=os.listdir(os.getcwd()+'\\Fedora project\\versions_diff')
diff_folders.sort()
for i in range( len(diff_folders) ):
  check_changes(diff_folders[i])