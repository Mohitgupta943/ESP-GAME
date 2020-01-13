import kivy
#kivy.require('1.10.1')
import kivy
from kivy.app import App
import _pickle as pickle
import glob
import os
from os import path
from kivy.uix.screenmanager import ScreenManager,Screen
from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput 
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from datetime import datetime,date
from kivy.graphics import Rectangle, Color 
from kivy.uix.recycleview import RecycleView
import socket
from validate_email import validate_email
from firebase import firebase
from kivy.uix.image import Image, AsyncImage
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button 
from kivy.clock import Clock
import random
sm=ScreenManager()
screen1=Screen(name="signin_screen")

screen2=Screen(name="newuser_screen")

firebase = firebase.FirebaseApplication('https://python-test-3130a.firebaseio.com/', None)
Current_task=0
class WindowManager(ScreenManager):
    pass





class ProblemsLayout(GridLayout): #This Class is responssible for creating layout for problems page 
    def __init__(self,q_no,task_no,user_email ,**var_args): 
        super(ProblemsLayout, self).__init__(**var_args) 

        self.cols = 1    
        self.spacing=50
        self.padding=80
        #print(task_no,q_no)
        src="Tasks\Task"+str(task_no)+"\Q"+str(q_no)+"\\"
        primary_image = Image(source = src+"P.jpg")
        self.add_widget(primary_image)

        #calling grid Layout
        im=MiniProblemsLayout(q_no,src,task_no,user_email)
        self.add_widget(im)

        next_button=Button(text='Next')
        next_button.bind()
    
class MiniProblemsLayout(GridLayout): # This class Creates the options in the layout for primary image
    Local_file_src=""
    ques_src=""
    def __init__(self,q_no,src,task_no,user_email, **var_args): 
        super(MiniProblemsLayout, self).__init__(**var_args) 

       
        self.Local_file_src='AllUsers\\'+user_email+'\Task'+str(task_no)+'\Q'
        self.ques_src=self.Local_file_src+str(q_no)
        self.cols = 3    
        self.spacing=20
        self.padding=20
        im1=MyButton(src+'S1.jpg')
        self.add_widget(im1)
        im2=MyButton(src+'S2.jpg')
        self.add_widget(im2)
        im3=MyButton(src+'S3.jpg')
        self.add_widget(im3)

        im1.bind(on_press=self.Pressed_1)
        im2.bind(on_press=self.Pressed_2)
        im3.bind(on_press=self.Pressed_3)
        
    def Pressed_1(self,x):
        print('Selected 1')
        f=open(self.ques_src,'w')
        f.write("1")
        f.close()

    def Pressed_2(self,x):
        print('Selected 2')
        f=open(self.ques_src,'w')
        f.write("2")
        f.close()

    def Pressed_3(self,x):
        print('Selected 3')
        f=open(self.ques_src,'w')
        f.write("3")
        f.close()

class MyButton(ButtonBehavior, Image): #This class is for creating Image Button which user clicks to select the option for questions
    def __init__(self,x, **kwargs):
        #print("4")
        super(MyButton, self).__init__(**kwargs)
        self.source = x
        self.allow_stretch=True
        self.size_hint=self.size
        

    def on_release(self):
        pass
       

    
class ProblemsPage(Screen):  # This class is responsible for complete question screen and its functionality
    Q=1
    Current_task=0
    Current_user_email=""
    def __init__(self,**kwargs):
      
        super(ProblemsPage, self).__init__(**kwargs)

        
        self.Refresh_Question()
        self.Q=1

    def Refresh_Question(self):
        User_data=self.Get_CurrentTask() #to get current task which user need to execute
        self.Current_task=User_data[1]
        self.Current_user_email=User_data[3]
        question_no=self.Q

        but_text=""
        Next_button=None

        if question_no<5:
            but_text="Next"
            Next_button=Button(text=but_text,background_color=(0.9,0.5,0.5,0.7),size_hint=(0.4,0.1),pos_hint={'x':0.6,'y':0.03})
        else:
            but_text="Submit"
            Next_button=Button(text=but_text,background_color=(0,7.4,0.7,0.5),size_hint=(0.4,0.1),pos_hint={'x':0.6,'y':0.03})

        t=ProblemsLayout(question_no,self.Current_task,self.Current_user_email) #ProblemsLayout is class defined above responsible for creating
                                                                                # problem page layout 
        self.add_widget(t)
        Next_button.bind(on_press=self.Button_Next)
        self.add_widget(Next_button)

    def Button_Next(self,x):
        self.Q+=1 
        if self.Q<=5:
            
            ProblemsPage.clear_widgets(self)
            self.Refresh_Question()
        else:
            self.Q=1
            self.Update_Local_Files()
            ProblemsPage.clear_widgets(self)
            self.Refresh_Question()
            msg="RESPONSE RECORDED !!\n\n Points for this task will be given when you are\npaired with other user\n\n"
            msg1="You can complete other available tasks\n\n   OR  \n\n PLEASE Log out and come back to get your points"
            popup = Popup(title='USER GUIDE', content=Label(text=msg+msg1),size_hint=(None, None), size=(500, 500))
            popup.open()
            self.manager.current='dashboard_screen' 

    def Update_Local_Files(self):  # This function updates local files of user according to the response

        User_data=self.Get_CurrentTask()
        C_email=User_data[3]
        Task_no=User_data[1]

        #Update Task Status
        Local_file_src='AllUsers\\'+C_email+'\Task'+str(Task_no)+'\\'
        f=open(Local_file_src+"IsCompleted",'w')
        f.write("True")
        f.close()

        #Update Current Task in metadata
        C_user=User_data[0]
        f_hand=open(r'data\\'+C_user,'w')
        ctask=int(User_data[1])+1
        print("In SUBMIT UPDATE CURRENT TASK",f_hand,ctask)
        f_hand.write(User_data[0]+" "+str(ctask)+" "+User_data[2]+" "+User_data[3])
        f_hand.close()
    
    def Get_CurrentTask(self):
        
        f_hand=open(r'data\\AllUsers','r')
        lis=""
        All_Users=[]
        for line in f_hand:
            lis=line.rstrip()
            All_Users.append(lis)
        print(All_Users)
        C_user=All_Users[-1]
        print("Get_Current_User",C_user)
        if C_user!='AllUsers':

            f_hand=open(r'data\\'+C_user,'r')
            lis=""
            for line in f_hand:
                lis=line.split(" ")
            
        return lis


class Dashboard(Screen):
    Number_of_tasks=3
    global Current_task
    global Current_user
    global Current_points
    global Current_email
    def __init__(self, **kwargs):
        print("6")
       
        super(Dashboard, self).__init__(**kwargs)
        self.Refresh_DeshBoard(0)
        Clock.schedule_interval(self.Refresh_DeshBoard,3) #adjust the time Here for setting the function call interval   

    def Refresh_DeshBoard(self,dt):

        Dashboard.clear_widgets(self)
      
        f_hand=open(r'data\\AllUsers','r')
        lis=""
        All_Users=[]
        for line in f_hand:
            lis=line.rstrip()
            All_Users.append(lis)

        C_user=All_Users[-1]
  
        if C_user!='AllUsers':

            f_hand=open(r'data\\'+C_user,'r')
            lis=""
            for line in f_hand:
                lis=line.split(" ")

            #variable to upadte screen
            self.Current_user=lis[0]
            self.Current_task=int(lis[1])
            self.Current_points=int(lis[2])
            self.Current_email=lis[3]

            #Kivy adding all stuffs to screen
            point_label=Label(text="Points:",font_size='30',pos_hint={'x':-0.4,'y':0.4},color= (0.5, 0.5, 0, 1))
        
            point=Label(text=str(self.Current_points),font_size='30',pos_hint={'x':-.29,'y':0.4},color= (0.5, 0.5, 0, 1))

            Username_lable=Label(text=self.Current_user,font_size='30',pos_hint={'x':.29,'y':0.4},color= (0.5, 0.5, 0, 1))

            logout_button=Button(text="Log Out",background_color=(0.7,0,0,0.8),size_hint=(0.4,0.1),pos_hint={'x':0.6,'y':0.05})
            logout_button.bind(on_press=self.logout_pressed)
            task_button=None
            Y=0.8
            for i in range(1,self.Number_of_tasks+1):  #
                d=i/10
                Y=Y-(0.11)
                
                if i==self.Current_task:
                    task_button=Button(text="Task "+str(i),background_color=(0,7.4,0.7,0.5),size_hint=(0.6,0.1),pos_hint={'x':0.2,'y':Y})
                    task_button.bind(on_press=self.Solve_Task)
                else:
                    task_button=Button(text="Task "+str(i),size_hint=(0.6,0.1),pos_hint={'x':0.2,'y':Y})
                self.add_widget(task_button)

            self.add_widget(point_label)
            self.add_widget(point)
            self.add_widget(Username_lable)
            self.add_widget(logout_button)

    def Solve_Task(self,x):
        toPerform=self.Current_task
        self.manager.current='problemspage_screen'

    def logout_pressed(self,x):
        self.manager.current='singin_screen'
    




class SignIn(Screen): # This is the main class which is resposible to sync. online and offline data and to sign in user after authentication
    #  change these to Adjust Number of questions/task and number of taks
    Number_of_question=5
    Number_of_tasks=3

    TASK_NUM=0
    EMAIL=""
    PASSWORD="" 
    U_NAME=''

    def __init__(self, **kwargs):
        super(SignIn, self).__init__(**kwargs)

        self.Email_Input=TextInput(hint_text="Enter Email Id",font_size='16',size_hint=(0.6,0.1),pos_hint={'x':0.2,'y':0.7})
        self.add_widget(self.Email_Input)

        self.password_Input=TextInput(hint_text="Enter Password",password=True,font_size='16',size_hint=(0.6,0.1),pos_hint={'x':0.2,'y':0.55})
        self.add_widget(self.password_Input)

        signIn_button=Button(text="Sign In",size_hint=(0.9,0.1),pos_hint={'x':0.08,'y':0.3})
        creatAccount_button=Button(text="Create Account",size_hint=(0.9,0.1),pos_hint={'x':0.08,'y':0.18})
        self.add_widget(signIn_button)
        self.add_widget(creatAccount_button)
        
        signIn_button.bind(on_press=self.Sign_In)
        creatAccount_button.bind(on_press=self.Create_Account)

    Current_task=0
   
    def Create_Account(self,x): # if New User send him/her to create account page
        self.manager.current='newuser_screen'

    def Sign_In(self,x): # If existing user then synchronize his/her previous responses with firebase and allow to log in
       
        self.user_email_id=self.Email_Input
        self.user_pass=self.password_Input

        email_id=self.user_email_id.text
        password=self.user_pass.text
       
        isConnected=NewUser().Check_Connectivity() #check for Internet

        if isConnected:

            check_user,self.Current_task,Current_points,Current_user,Current_emailid= NewUser().Is_User_Already_registered(email_id,password,'Users')
            #Only users list
           
            self.EMAIL=Current_emailid
            self.PASSWORD=password 
            self.U_NAME=Current_user


            if check_user==False:
                self.manager.current="newuser_screen"
                popup = Popup(title='New User', content=Label(text="Please Create an Account and Try Again"),size_hint=(None, None), size=(400, 400))
                popup.open()
            else:
                f_hand=open(r'data\\'+Current_user,'r')
                lis=""
                for line in f_hand:
                    lis=line.split(" ")
                #variable to upadte screen
                #user=lis[0]
                # points=int(lis[2])
                # email=lis[3]
                task=int(lis[1])
                self.Synchronize_Databases(email_id,task,password,Current_user)
                #Clock.schedule_interval(self.cll_sync,30)
                check_user,self.Current_task,Current_points,Current_user,Current_emailid= NewUser().Is_User_Already_registered(email_id,password,'Users')
                print("CURRENT",task)
                f=open(r'data\\AllUsers','a+')
                f.write(Current_user+" \n")
            
                #individual user data
                f=open(r'data\\'+Current_user,'w')
                f.write(Current_user+" "+str(self.Current_task)+" "+str(Current_points)+" "+Current_emailid)
                if(task>self.Number_of_tasks):
                    msg="BINGO !!!!!\n\n\n You have completed all the tasks"
                    popup = Popup(title='USER GUIDE', content=Label(text=msg),size_hint=(None, None), size=(500, 500))
                    popup.open()
                else:
                    msg="PLEASE PLAY CAREFULLY !!\n\nYou get only one chance to complete each task\n\nAfter Submitting task You cannot edit your responses"
                    popup = Popup(title='USER GUIDE', content=Label(text=msg),size_hint=(None, None), size=(500, 500))
                    popup.open()
                self.manager.current='dashboard_screen'

        else:
            popup = Popup(title='No Internet', content=Label(text="Try when connected"),size_hint=(None, None), size=(400, 400))
            popup.open()

        print(isConnected)

        print(email_id,password)



    def Synchronize_Databases(self,user_email,task_no,password,u_name): 
        
        #This function syncronizes online and offline data to maintain consistency and  Persistence

        print("In SYNCHRONIZATION"+u_name)

        data=firebase.get("python-test-3130a/Users","")

        Local_file_src='AllUsers\\'+user_email+'\Task'

        d={} #for retriving users loacl responses from file

        for i in range(1,self.Number_of_tasks+1):
            src=Local_file_src+str(i)+"\\"
            f=open(src+"IsEvaluated",'r')
            S=""
            for line in f:
                S=line.split(" ")
            f.close()
            isevaluated=S[0]

            f=open(src+"IsCompleted",'r')
            s=""
            for line in f:
                s=line.split(" ")
            print("SSSSSS",s)
            f.close()

            if s[0]=='True' and isevaluated=='False':
                d['task_'+str(i)]={}
                for j in range(1,self.Number_of_question+1):
                    f=open(src+"Q"+str(j),'r')
                    res=""
                    for line in f:
                        res=line.split()
                    f.close()
                    d['task_'+str(i)]['Q'+str(j)]=int(res[0])
                d['task_'+str(i)]['isDone']=s[0]
                d['task_'+str(i)]['isEvaluated']=isevaluated


        f_hand=open(r'data\\'+u_name,'r')
        lis=""
        for line in f_hand:
            lis=line.split(" ")
        f_hand.close()

        Current_task=int(lis[1])

        f_hand.close()

        f=open(r'data\\'+u_name,'w')
        f.write(lis[0]+' '+str(Current_task)+' '+lis[2]+" "+lis[3])
        f.close()


        root="python-test-3130a/Users/"
        b='/'
        UID=""
        for i in data:
            com_point=0
            e=data[i]['Email']
            p=data[i]['Password']
            if (e==user_email and p==password): #if same user then sync all data
                UID=i
                for j in d: # j=task_x
                    X=data[i][j]
                    for k in X: # for task 1 questions
                        for qno in range(1,6):
                            #print(X[k]['Q'+str(qno)])
                            print("Syncing...",(root+i+b+j+b+k))
                            firebase.put(root+i+b+j+b+k,'Q'+str(qno),d[j]['Q'+str(qno)])

                        firebase.put(root+i+b+j+b+k,'isDone',d[j]['isDone'])
                        firebase.put(root+i+b+j+b+k,'isEvaluated',d[j]['isEvaluated'])
                
                firebase.put(root+i+b,'Current_task',Current_task)

        sec_email=""
        t_no=""
        D=[] #For refering to tasks
        for i in range(1,self.Number_of_tasks+1):
            D.append('task_'+str(i))

        #Evaluation and pairing players to give points

        for i in data:
            e=data[i]['Email']
            p=data[i]['Password']
            if (e!=user_email or p!=password): #if different user then match responses and give point to respective user
                sec_email=data[i]['Email']
                #print(data[i]['Email'],data[i]['Password'])
                for j in D: # j=task_x
                    t_no=j[-1]
                    com_point=0
                    Myself=data[UID][j]
                    Sec_User=data[i][j]
                    for k in Myself : # for task 1 questions
                        if (Myself[k]['isDone']=='True' and Myself[k]['isEvaluated']=='False') : #If I have Done that question
                            for M in Sec_User:
                                if (Sec_User[M]['isDone']=='True' and Sec_User[M]['isEvaluated']=='False') :#If Other User have Done that question
                                    #Match responses and allot points to both users
                                    for qno in range(1,6):
                                        
                                        if Sec_User[M]['Q'+str(qno)]==Myself[k]['Q'+str(qno)]:
                                            com_point+=1
                                            print("Match found")
                                    firebase.put(root+i+b+j+b+M,'isEvaluated','True')
                                    firebase.put(root+UID+b+j+b+k,'isEvaluated','True')
                                    print('Updated...istrue',root+i+b+j+b+M,'isEvaluated','True')
                                    print('Updated...istrue',root+UID+b+j+b+k,'isEvaluated','True')

                                    p_point=int(data[UID]['Points'])+com_point
                                    s_point=int(data[i]['Points'])+com_point
                                    print("points.....",data[i]['Points'],data[UID]['Points'])
                                    firebase.put(root+i+b,'Points',s_point)
                                    firebase.put(root+UID+b,'Points',p_point)

                                    src1='AllUsers\\'+sec_email+'\Task'+t_no+'\isEvaluated'
                                    f=open(src1,'w')
                                    f.write('True')
                                    f.close()
                                    src2='AllUsers\\'+user_email+'\Task'+t_no+'\isEvaluated'
                                    f=open(src2,'w')
                                    f.write('True')
                                    f.close()                      

                    
                            
    
                          
                                           
class NewUser(Screen):

    # Change these to Adjust number of questions and Number of tasks
    Number_of_question=5
    Number_of_tasks=3

    def Register_User(self):
        
        isconnected=self.Check_Connectivity()

        if not isconnected:
            popup = Popup(title='No Internet', content=Label(text="Try when connected"),size_hint=(None, None), size=(400, 400))
            popup.open()
            print(isconnected)
        else:
            #Taking input values feeded by User
            user_email_id=ObjectProperty(None)
            user_pass=ObjectProperty(None)
            user_name=ObjectProperty(None)
            
            # texts from kivy
            email_id=self.user_email_id.text
            password=self.user_pass.text
            username=self.user_name.text

            #Error messages
            is_valid = validate_email(email_id)
            name_error=""
            email_error=""
            password_error=""
            allok=True

            if username is None or len(username)<=1:
                name_error="User Name must have atleast 3 characters\n\n"
                allok=False
            if is_valid==False:
                email_error="Entered email is invalid\n\n"
                allok=False
            if password.isalnum()==False or len(password)<5:
                password_error="Password must be alphanumeric and have alteast 5 characters"
                allok=False

            if allok==False:
                Error_Message=name_error+email_error+password_error
                popup = Popup(title='Invalid Entry', content=Label(text=Error_Message),size_hint=(None, None), size=(500, 500))
                popup.open()

            else:

                #Check if User alredy registered and extract relevant values
                alrady_registered,current_task,Current_points,Current_user,Current_emailid=self.Is_User_Already_registered(email_id,password,"Users")
                if alrady_registered==True:
                    popup = Popup(title='Sign In', content=Label(text="User Already Exist. Please Sign In"),size_hint=(None, None), size=(400, 400))
                    popup.open()

                else:

                    all_users=open(r'data\\Users','a')
                    all_users.write(email_id+" "+password+"\n\n")
                    all_users.close()

                    f=open(r'data\\'+username,'w')
                    print("FFFF",f,username,current_task)
                    f.write(username+' '+str(current_task)+" "+str(Current_points)+" "+email_id)
                    f.close()

                    root="python-test-3130a/Users"
                    user_data={'User_Name':username,'Email':email_id,'Password':password,'Points':0,'Current_task':1}
                    
                    # Create A folder with Users emailid as name to record user's response locally 
                    if not os.path.exists('AllUsers'):
                        os.makedirs('AllUsers')
                    if not os.path.exists('AllUsers\\'+email_id):
                        os.makedirs('AllUsers\\'+email_id)

                    #Pushing Users info to firebase and create account
                    result=firebase.post(root,user_data)
                    UID=result['name']
                    for i in range(1,self.Number_of_tasks+1):
                        task_qus={}
                        if not os.path.exists('AllUsers\\'+email_id+'\Task'+str(i)):
                            os.makedirs('AllUsers\\'+email_id+'\Task'+str(i))
                        for j in range(1,self.Number_of_question+1):
                            fil=open('AllUsers\\'+email_id+'\Task'+str(i)+'\Q'+str(j),'w')
                            fil.write("-1")
                            fil.close()
                            question_id="Q"+str(j)
                            task_qus[question_id]=0
                        fil=open('AllUsers\\'+email_id+'\Task'+str(i)+'\IsCompleted','w')
                        fil.write("False")
                        fil.close()
                        fil=open('AllUsers\\'+email_id+'\Task'+str(i)+'\IsEvaluated','w')
                        fil.write("False")
                        fil.close()
                        task_qus['isEvaluated']=False
                        task_qus['isDone']=False
                        firebase.post(root+'/'+UID+'/task_'+str(i),task_qus)

                    #print(result)
                    popup = Popup(title='Registered', content=Label(text="Successfully Registered, Please Sign In"),size_hint=(None, None), size=(450, 450))
                    popup.open()
                    print(isconnected)
    
    def Is_User_Already_registered(self,email_id,password,Node):
                data=firebase.get("python-test-3130a/"+Node,"")
            
                  
                print(data)
                isuser=False
                current_task=0
                current_points=0
                current_user=''
                current_emailid=''
                if data is not None:
                    for i in data:
                        # Retriving data from Firebase
                        n=data[i]['Email'] 
                        p=data[i]['Password']
                        current_task=data[i]['Current_task']
                        current_points=data[i]['Points'] 
                        current_user=data[i]['User_Name'] 
                        current_emailid=data[i]['Email']
                       
                        if n==email_id and password==p:
                            isuser=True
                            uid=i
                            break
                            
                    if isuser==True:
                        return True,current_task,current_points,current_user,current_emailid
                    else:
                        
                        return False,1,0,'NoUser','Email'

                return False,1,0,'NoUser','Email'

    def Check_Connectivity(self,host="8.8.8.8", port=53, timeout=3): #for checking Internet connectivity
        """
        Host: 8.8.8.8 (google-public-dns-a.google.com)
        OpenPort: 53/tcp
        Service: domain (DNS/TCP)
        """
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            return True
        except socket.error as ex:
            print(ex)
            return False

kv=Builder.load_file("esp.kv") #reference to kivy file
class Withkivy(App):
    def build(self):
        return kv


if __name__=="__main__":
    Withkivy().run()