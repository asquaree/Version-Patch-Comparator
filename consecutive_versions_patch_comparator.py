# -*- coding: utf-8 -*-

# pip install gitpython
# pip install shutil
# pip install os
# pip install subprocess
# pip install csv


#Importing libraries

from git import Repo
import os
import shutil
import subprocess
import csv


#FUNCTIONS

#Function to get repository name

def get_repository_name(repository_link):
  repository_name=""
  i=len(repository_link)-1
  while(repository_link[i]!='.'):
    i=i-1
  i=i-1
  while(repository_link[i]!='/'):
    repository_name+=repository_link[i]
    i=i-1
  repository_name=repository_name[::-1]
  return repository_name

    
  
#Function to fetch branches name

#USAGE CLI
def clone_repo(repository_link,repository_name):

  # if  os.path.exists(os.getcwd()+'\\Repository'):
  #   shutil.rmtree(os.getcwd()+'\\Repository')

  #repository_name=str(repository_link,repository_name)
  subprocess.run(['git', 'clone',repository_link,"Cloned"],cwd=os.getcwd()+"\\"+ repository_name,stdout=subprocess.DEVNULL)# cloning the repository inside the Fedora project folder


def get_branches_name(repository_name): 
  stdout = subprocess.check_output('git branch -r'.split(),cwd=os.getcwd()+"\\"+ repository_name+'\\'+ "Cloned") #fetching all branches names
  out = stdout.decode()
  all_branches = [b.strip('* ') for b in out.splitlines()]
  
  branches_name=[] #will store branch names
  for i in range(10,len(all_branches)-10):
    branch_name=''
    all_branches[i]=all_branches[i][::-1]
    j=0
    while(all_branches[i][j]!='/'):
      branch_name+=all_branches[i][j]
      j+=1
    branch_name=branch_name[::-1]
    if(branch_name[0]=='f'):
      branches_name.append(branch_name)
  branches_name=sorted(branches_name)

  return branches_name

#Function to add empty patch file in the branch

def add_emptyfile(path,branch):
  file = 'emptyfile'+branch+'.patch'
  with open(os.path.join(path, file), 'w') as fp:
    pass

#Function to clone single single branch from the repository and storing it making different folders

def create_branch_folder(branches_name,repository_insidefolder_name,repository_name):
    print('fetching branches........')
    for i in range(len(branches_name)):
      branch=branches_name[i]
      destination_path= os.getcwd()+"\\"+ repository_name+'\\'+'\\Branches\\'+branch
      subprocess.run(['git','checkout', branch],cwd=os.getcwd()+"\\"+ repository_name+'\\'+repository_insidefolder_name,stdout=subprocess.DEVNULL)
      source_path=os.getcwd()+"\\"+ repository_name+'\\'+'\\'+repository_insidefolder_name
    
      branch_patch_files=os.listdir(source_path)
      shutil.copytree(source_path,destination_path)
      add_emptyfile(destination_path,branch)#adding an empty patch file in the folder
    

#Function to compare consecutive Branches

def consecutive_compare(branches,repository_name):
  print("Comparing Branches....")
  for i in range(len(branches)-1):
    compare(branches[i],branches[i+1],repository_name) # function to compare 2 Branches

#Function to compare 2 Branches

def compare(branch1,branch2,repository_name):
  diff_dir_name=""+branch1+branch2
  folder_name="Branches_diff"
  diff_dir_parent_dir=os.getcwd()
  if not os.path.exists(os.getcwd()+"\\"+ repository_name+'\\'+"\\"+folder_name):
    os.mkdir(os.path.join(os.getcwd()+"\\"+ repository_name,folder_name)) # creating a branch diff folder whih will contain all diff folders(For eg f11f10)
  diff_dir_parent_dir+='\\'+folder_name
  diff_dir_path = os.path.join(os.getcwd()+"\\"+ repository_name+'\\'+folder_name, diff_dir_name)
  os.mkdir(diff_dir_path)# creating diff folder(For eg f11f10)

  path1=os.getcwd()+"\\"+ repository_name+'\\'+"\\Branches\\"+branch1
  path2=os.getcwd()+"\\"+ repository_name+'\\'+"\\Branches\\"+branch2
  branch1_patch_files={} # creating a dictionary which will keep a check of same patch files name among 2 Branches
  for file in os.listdir(path1):
    if file.endswith(".patch"):
        branch1_patch_files[file]=1
  for file in os.listdir(path2):
    if file.endswith(".patch"):
      #print(file)
      if file in branch1_patch_files.keys():
        branch1_patch_files[file]=2
        branch1_file=path1+"\\"+file
        branch2_file=path2+"\\"+file
        find_diff(branch1_file,branch2_file,diff_dir_path,str(file)) #find diff between 2 patch files
        
      else:
        branch2_file=path2+"\\"+file
        branch1_file=path1+"\\"+'emptyfile'+branch1+'.patch'
        find_diff(branch1_file,branch2_file,diff_dir_path,str(file))

  for file in branch1_patch_files.keys():
    if branch1_patch_files[file]==1:
      branch2_file=path2+"\\"+'emptyfile'+branch2+'.patch'
      branch1_file=path1+"\\"+file
      find_diff(branch1_file,branch2_file,diff_dir_path,str(file))

def compare_patch(branch1,branch2,patch,repository_name):
  diff_dir_name=""+branch1+branch2
  folder_name="Branches_diff"
  diff_dir_parent_dir=os.getcwd()
  if not os.path.exists(os.getcwd()+"\\"+ repository_name+'\\'+"\\"+folder_name):
    os.mkdir(os.path.join(os.getcwd()+"\\"+ repository_name,folder_name)) # creating a branch diff folder whih will contain all diff folders(For eg f11f10)
  diff_dir_parent_dir+='\\'+folder_name
  diff_dir_path = os.path.join(os.getcwd()+"\\"+ repository_name+'\\'+folder_name, diff_dir_name)
  os.mkdir(diff_dir_path)# creating diff folder(For eg f11f10)

  path1=os.getcwd()+"\\"+ repository_name+'\\'+"\\Branches\\"+branch1
  path2=os.getcwd()+"\\"+ repository_name+'\\'+"\\Branches\\"+branch2
  file=patch

  if file in os.listdir(path1):
    if file in os.listdir(path2):
      branch1_file=path1+"\\"+file
      branch2_file=path2+"\\"+file
      find_diff(branch1_file,branch2_file,diff_dir_path,str(file)) #find diff between 2 patch files
    else:
      branch2_file=path2+"\\"+'emptyfile'+branch2+'.patch'
      branch1_file=path1+"\\"+file
      find_diff(branch1_file,branch2_file,diff_dir_path,str(file))
  else:
    branch2_file=path2+"\\"+file
    branch1_file=path1+"\\"+'emptyfile'+branch1+'.patch'
    find_diff(branch1_file,branch2_file,diff_dir_path,str(file))
    

#Function to find diff between 2 files and storing it into diff folder For eg F10F11 creating same patch name file

def find_diff(file1,file2,diff_dir_path,file):
    #PIPE = subprocess.PIPE
    branch1=file1
    branch2=file2
    with open(os.path.join(diff_dir_path, file),'w') as f:
      process = subprocess.run(['git', 'diff', '--no-index',branch1,branch2], stdout=f,text=True,stderr=subprocess.DEVNULL) # creating a file named as the patch name storing diff
      #print(process.stdout)
    #stdoutput, stderroutput = process.communicate()

    # if 'fatal' in stdoutput:
    #   # Handle error case
    #   pass
    # else:
    #   # Success!
    #   pass

#Function to count added deleted and number of lines in diff file

def count_lines(diff,path):
  added_lines=0
  deleted_lines=0
  #total_lines=0
  infile = open(os.path.join(path,diff), 'r', encoding='mac_roman')
  text = infile.readlines()
  for j in (text):
    if(j[0]=='+'):
      added_lines+=1
    elif(j[0]=='-'):
      deleted_lines+=1
    #total_lines+=1
  if added_lines!=0 or deleted_lines!=0 :
    added_lines-=1
    deleted_lines-=1
  
  return added_lines,deleted_lines

#Initializing csv file

def int_csv():
  fields=['repository_name','path_file','branch1','branch2','added_lines','deleted_lines','is_deleted']
  csv_name="comparison_sheet.csv"
  with open(os.path.join(os.getcwd(),csv_name), 'w') as csvfile:
    csvwriter = csv.writer(csvfile) 
    csvwriter.writerow(fields)
  return csv_name


#Function to fetch added lines, deleted lines,patch name and is deleted from a diff folder For eg f10f11 and insert it into excel sheet

def check_changes(branch_diff,csv_name, repository_name):
  path=os.getcwd()+"\\"+ repository_name+'\\'+'\\Branches_diff'+'\\'+branch_diff
  for diff in os.listdir(path):
    patch_name=str(diff)
    #print(patch_name)
    brch_diff=str(branch_diff)
    brch_diff_len=len(brch_diff)/2
    branch1=brch_diff[0:int(brch_diff_len)]
    branch2=brch_diff[int(brch_diff_len):]
    added_lines,deleted_lines=count_lines(diff,path) # storing added,deleted lines values
    #print(added_lines)
    #print(deleted_lines)
    #print(total_lines)
    isdeleted=0
    if(deleted_lines!=0 and added_lines<=1):
      isdeleted=1
    with open(os.path.join(os.getcwd(),csv_name), 'a') as csvfile: #writing the information into the csv for each diff file
      csvwriter = csv.writer(csvfile)
      csvwriter.writerow([repository_name,patch_name,branch1,branch2,added_lines,deleted_lines,isdeleted])

#void main()
#USAGE CLI
def compare_consecutive_branches(repository_link):

  
  repository_name=get_repository_name(repository_link)
  print(repository_name)
  if not os.path.exists(os.getcwd()+"\\" + repository_name):#Creating folder with repository's name 
    os.mkdir(os.path.join(os.getcwd(),repository_name))
  
  clone_repo(repository_link,repository_name)
  if not os.path.exists(os.getcwd()+"\\" + repository_name+"\\" +"Branches"):
    os.mkdir(os.path.join(os.getcwd()+"\\" + repository_name,"Branches")) #creating Branches folder inside repository folder
  
  branches_name=get_branches_name(repository_name) #fetching branch names from the branches
  print('Branches:\n')
  print(branches_name)

  print(os.getcwd())
  
  create_branch_folder(branches_name,"Cloned",repository_name)#cloning Branches seperately from the repository 
  
  branches = os.listdir(os.getcwd()+"\\"+repository_name+'\\Branches')#fetching all the branches from the branches folder
  branches.sort()

  consecutive_compare(branches,repository_name) # function to compare consecutive branches
  
  print("Creating csv file....")
  csv_name=int_csv() #initializing csv file with the headers

  diff_folders=os.listdir(os.getcwd()+"\\"+repository_name+'\\Branches_diff') #storing all diff folders
  diff_folders.sort()
  for i in range( len(diff_folders) ):
    check_changes(diff_folders[i],csv_name,repository_name) #checking changes in each diff file inside a folder
  
  os.startfile(os.getcwd()+"\\"+csv_name)


#USAGE CLI
def compare_2_branches(repository_link,branch1,branch2):

  repository_name=get_repository_name(repository_link)
  print(repository_name)

  
  folder_name="versions"
  
  if not os.path.exists(os.getcwd()+"\\" + repository_name+"\\" +folder_name):
    os.mkdir(os.path.join(os.getcwd()+"\\" + repository_name,folder_name)) #creating versions folder
  
  
  clone_repo(repository_link,repository_name)
  version1=str(version1)
  version2=str(version2)
  all_version=[version1,version2]

  print('Version:\n')
  print(all_version)
  
  get_version(all_version,"Cloned",repository_name)#cloning versions seperately from the repository 
  
  branches = os.listdir(os.getcwd()+"\\"+repository_name+'\\versions')#fetching all the versions from the versions folder
  branches.sort()

  consecutive_compare(branches,repository_name) # function to compare consecutive versions
  
  print("Creating csv file....")
  csv_name=int_csv() #initializing csv file with the headers

  diff_folders=os.listdir(os.getcwd()+"\\"+repository_name+'\\versions_diff') #storing all diff folders
  diff_folders.sort()
  for i in range( len(diff_folders) ):
    check_changes(diff_folders[i],csv_name,repository_name) #checking changes in each diff file inside a folder
  
  os.startfile(os.getcwd()+"\\"+csv_name)

#USAGE CLI  
def compare_2_patches(repository_link,version1,version2,patch):

  repository_name=get_repository_name(repository_link)
  print(repository_name)

  
  folder_name="versions"
  
  if not os.path.exists(os.getcwd()+"\\" + repository_name+"\\" +folder_name):
    os.mkdir(os.path.join(os.getcwd()+"\\" + repository_name,folder_name)) #creating versions folder

  
  clone_repo(repository_link,repository_name)
  version1=str(version1)
  version2=str(version2)
  all_version=[version1,version2] #only 2 versions

  print('Version:\n')
  print(all_version)

  get_version(all_version,"Cloned",repository_name)#cloning versions seperately from the repository 
  
  branches = os.listdir(os.getcwd()+"\\"+repository_name+'\\versions')#fetching all the versions from the versions folder
  branches.sort()

  compare_patch(version1,version2,patch,repository_name) # function to compare consecutive versions

  print("Creating csv file....")
  csv_name=int_csv() #initializing csv file with the headers

  diff_folders=os.listdir(os.getcwd()+"\\"+repository_name+'\\versions_diff') #storing all diff folders
  diff_folders.sort()
  for i in range( len(diff_folders) ):
    check_changes(diff_folders[i],csv_name,repository_name) #checking changes in each diff file inside a folder
  
  os.startfile(os.getcwd()+"\\"+csv_name)



if __name__=="__main__":
  repository_link=input('Enter the repository git link:')
  compare_consecutive_branches(repository_link)
  
  