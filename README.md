# MonkeyGit
- - -
## Objective:
``` 
Implement a git like client system with limited capabilities. The program should be able
• to create/initialize a git repository, creating a .git folder with the necessary details.
• to add files to index and commit, maintaining the commit-ids so that retrieving them
back could be done.
• to see the status, diff, checkout previous commits, as shown by the git utility.
```

## Commands Implemented:
- - -
* ###  git cd : To change the current working directory for git initialisation
* #### Command Syntax:
```
git cd /home/krati/GitTest
```
* ### git init : creating .git-vcs repository in current working directory
* #### Command Syntax:
```
git init
```
* ### git status : shows tracked,untracked,modified and deleted status for files under git directory
* #### Command Syntax:
```
git status
```
* ### git add : add specific files or whole working directory (in case '.' given)
* #### Command Syntax:
```
git add . 
git add <filename>
```
* ### git commit : commit the added/tracked files i.e. previously added using git add command
* #### Command Syntax:
```
git commit -m "<commit message>"
```
* ### git rollback : used for undoing changes to a repository's commit history
* #### Command Syntax:
```
git rollback -c <commit id>
git rollback -c -s , s for no of steps
```
* ### git push : upload commit repository content to a remote repository
* #### Command Syntax:
```
git push
```
* ### git pull : download content from a remote, update the local repository to that content
* #### Command Syntax:
```
git pull
```
* ### git diff : difference between untracked and tracked version of a file
* #### Command Syntax:
```
git diff <filename>
```
* ### git rm : change tracked files to untrack
* #### Command Syntax:
```
git rm .
git rm <filename>
```
* ### git log : print the logged comments
* #### Command Syntax:
```
git log
```
---
Project Setup
---
* ### Clone the project
```
https://github.com/yash-pathak-1997/AOS-Project-VCS.git
```
* ### Run the project
```
 python3 -m streamlit run  main.py
```
