# ESP-GAME
Esp game
To run this project you need to satisfy following requirements:
1. Python3
2. Kivy 1.11.1
3. Firebase

 Also go through the requiremets.txt file and install required dependencies. I have provide link for the solution of potential error.
Please ensure all the imports and assure that all imports are present or kindly install them(mostly by pip install xyz)
To run this project simply download/clone the Project folder from the repo.
After that simply run Esp.py file (python Esp.py)

For this project I have following Assumptions:
1. Images to be shown in problems are stored locally(it can also be stored on the firebase/server) in a folder named  Tasks in the following fashion:

Tasks/Task1/Q1...Q5'  and  Q1 also contain 4 images (1 primary and 3 secondary)
Tasks/Task2/Q1...Q5'  and  Q1 also contain 4 images (1 primary and 3 secondary) 
 
 
 
 2. At the time of login or creating accound Internet is required. After signing in Internet is not required i.e Player will be able to play and complete tasks whether Internet is available or not. 
 
The user's response is saved in both firebase and on local file system. Whenever a user creats account his/her data is saved in folders named 'data' and 'AllUsers'.
 
The files for now are not encrypted but for adding security we can add encryption to the files.

3. For getting score for any or all submited task user is required to log out and log in. As only on login Internet is required so above step is required in order to push user's response to server and match it with other user's response and evaluate.

4.For now only three tasks (Each task has 5 primary questions/images) is considered. It can be varied according to the requirements.

5.This game works fine for N number of users.

6. Each users gets only one chance to perform one task.

At a time only one task is unlocked(That is green colored) and rest are locked. Other tasks are unlock sequentially as the users progresses.

In firebase I have followed following hierarchy:
              Users(root)--->User(1)--->{user_name, emailid, password, current_task_performing, points, task1{}, task2{},....taskn{})
              
 GamePlay:
When you start the task you will see a primary image and 3 secondary images. You need to select the most relevent image and click on it.
Once you complete all the questions you can submit it.

NOTE:
Current code is designed for running on single system with multiple users. If you want to run it on different systems you need to do following changes:
You need to comment few lines in Esp.py (from line no. 500 to 503):

500.src1='AllUsers\\'+sec_email+'\Task'+t_no+'\isEvaluated'

501.f=open(src1,'w')

502.f.write('True')

503.f.close()

COMMENT above line in Esp.py 

 Flow of project:
 
 1. signin/create acoount (Proper validation and authentication) at the time of sign in online and offline databases are synced.
 ![](Images/newuser.png)
 
 2. Dashboard displayes user name 
 ![](Images/Dash.png)
 
 
 3. Task problems                                
 ![](Images/Problems.png)  
 
 4. Firebase Architecture
 
 ![](Images/Firebase.png)
 
 
 
                  

