# compatibility-project

>In this project,we have developed a comparator which compares branches and patches within the git repository and showcases the output in the form of a csv file.The API is called through the command line interface created to perform 4 possible usages

## Process
1. As soon as you perform any usage,the application will clone the repository to your local machine where location of the folder is same as the location of the program.
2. A folder named 'Branches' will create which will consist if sub folders named after the branches which you want to comapre.Each sub branch folder will contain patch files of the particular branch which are copied from the repository.
3. A 'Diff' folder will create which will consist of sub folders named after the 2 branches which wanted to compare for eg 'f10f11'.These sub diff folders will contain diff patch files.
4. A will csv generate having 7 columns['repository_name','path_file','branch1','branch2','added_lines','deleted_lines','is_deleted'].Is deleted will be a boolean value(1 or 0).1 if the patch is not present in the later branch.

### Usage
1. Clone the repository to the local - clone_repository <repository_link>
2. Compare consecutive branches - compare_consecutive_branches <repository_link>
3. Compare 2 particular branches - compare_branches <repository_link> <branch1> <branch2>
4. Compare a particular patch of 2 particular branches - compare_branches_patch <repository_link> <branch1> <branch2> <patch>

### Installing / Getting started
    
```shell
1.make sure that git is installed in your pc
2.make sure that python3 is installed in your pc
```
### Developing

``` shell
1. run - git clone https://github.com/justina777/compatibility-project.git
2. set the current directory to the cloned repository
3. run -python diff_patch_driver.py "Usage"
```  
  You need to choose a particular usage from 'Usage' according to your need.As soon as you run the command,3 folders will create and a csv will automatically open.
  

### Configuration 
  
  #### Argument
  `python diff_patch_driver.py <usage> <repository_link> <branch1> <branch2>`<br>
  Example: 
  ```shell
  python diff_patch_driver.py compare_branches https://src.fedoraproject.org/rpms/firefox.git f12 f13
  ```
  where 'diff_patch_driver.py' is the CLI filename ,'compare_branches' is the defined command to compare 2 particular branches 'https://src.fedoraproject.org/rpms/firefox.git' is the repository link and 'f12' 'f13' are the branches name.
  
### Tools
  1. python
  2. git

### Output
  
  1.Terminal output-![image](https://user-images.githubusercontent.com/53035125/128768201-413d7cf3-98d7-4f27-8da3-4e9102a58602.png)
2.Csv generated -![image](https://user-images.githubusercontent.com/53035125/128768420-b55fa50c-8599-4e08-8671-35a37fdf0903.png)


  
  
  
  
 
