# ESP-GAME
Esp game
To run this project you need to satisfy following requirements:\n
1. Python3
2. Kivy 1.11.1
3. Firebase\n
To run this project simply run esp.py. 
For this project I have following Assumptions:
1. Images to be shown in problem are stored locaaly(it can also be stored on the firebase) in a folder named  Tasks in the following fashion:\n
 Tasks/Task1/Q1...Q5'  and  Q1 also contain 4 images (1 primary and 3 secondary)
 Tasks/Task2/Q1...Q5'  and  Q1 also contain 4 images (1 primary and 3 secondary) 
 
 I have added Task1 in Tasks folder for referance.
 
 2. At the time of login or creating accound Internet is required
 
 The user's response is saved in both firebase and on local file system. Whenever a user creats account his/her data is saved in folders named 'data' and 'AllUsers' (These folders are created at run time).
 
The files for now are not encrypted but for adding security we can add encryption to the files.

In firebase I have followed following hierarchy:
              Users(root)--->User(1)--->{user_name, emailid, password, current_task_performing, points, task1{}, task2{},....taskn{})
              
 Flow of project:
 
 1. signin/create acoount (Proper validation and authentication) at the time of sign in online and offline databases are synced.
 ![](Images/newuser.png)
 
 2. Dashboard displayes user name 
 ![](Images/Dash.png)
 
 
 3. Task problems
 ![](Images/Problems.png)
 
                  

