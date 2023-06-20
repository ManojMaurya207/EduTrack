
from customtkinter import *
import tkinter as tk
from PIL import ImageTk,Image
from datetime import *
import time
import pymysql
from tkinter import ttk
import wikipedia
import random
import speech_recognition as sr
import pyttsx3
import tkinter.messagebox as messagebox
student_id=104
#database connect
db=pymysql.connect(host='localhost',user='root',password='root',database='student_database',charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)

#datetime
def date_time_display():
        
        def ct_time():
            now = datetime.now()
            ct_string = now.strftime("%H:%M:%S")
            return ct_string

        def ct_change():
            ct_string = ct_time()
            time_lb.configure(text=ct_string)
            f0.after(1000, ct_change)  # update every 1 second
        #logout_frame
        def logout_frame():
            delete_frames()
            date_time_display()
            def destroy_window():
                student_win.destroy()
            #asking to logout
            log_lb=CTkLabel(f0,text="Do you want to logout ?",font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
            log_lb.place(relx=0.5,y=200,anchor=CENTER)
            log_bu=CTkButton(f0,text="Yes",height=45,command=destroy_window,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
            log_bu.place(relx=0.5,y=300,anchor=CENTER)

        today = datetime.today()
        t_date= today.strftime("%B %d, %Y")
        #date and time 
        d_f=CTkFrame(f0,width=350,height=50,border_color="black",border_width=3,fg_color="white",corner_radius=40)
        d_f.place(x=730,y=5)
        time_lb=CTkLabel(d_f,width=110,height=30,text="",font=CTkFont("Helvetica",19),fg_color="white",corner_radius=40,text_color="black")
        time_lb.place(relx=0.8,rely=0.5,anchor=CENTER)
        date_lb=CTkLabel(d_f,text=t_date,width=150,height=30,corner_radius=8,font=("Helvetica",20),text_color="black",bg_color="white")
        date_lb.place(relx=0.3,rely=0.5,anchor=CENTER)
        ct_change()

        photo1=CTkImage(Image.open("logout1.png"),size=(50,50))
        edit_b=CTkButton(f0,image=photo1,command=logout_frame,text="",hover_color="#E0E0EB",cursor="hand2",width=20,height=40,fg_color="#66B3FF",corner_radius=10)
        edit_b.place(x=1100,y=0)
#Treeview
def treeview():
        f91=CTkFrame(f0,width=925,height=555,fg_color="white",border_width=3,corner_radius=12,border_color="black")
        f91.place(x=130,y=110)
        f9=CTkFrame(f0,width=90,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
        f9.place(x=140,y=120)
        f8=CTkFrame(f9,width=100,height=540,fg_color="white",border_width=3,corner_radius=12,border_color="black")
        f8.pack()
        cursor=db.cursor()
        cursor.execute("SELECT teacher.teacher_id,teacher.name,teacher.quali ,teacher.phone_no,subject.sub_name FROM teacher, class , teach_class , subject where teacher_id=teacher_code and sub_id=sub_code and std_id=std_code and std_id=%s",(Std))
        data=cursor.fetchall()
        teach_id=[]
        teach_name=[]
        teach_quali=[]
        teach_phone=[]
        subject_name=[]

        for i in data:
                teacher_id=i.get("teacher_id")
                teacher_name=i.get("name")
                teacher_quali=i.get("quali")
                sub_name=i.get("sub_name")
                
                teach_id.append(teacher_id)
                teach_name.append(teacher_name)
                teach_quali.append(teacher_quali)
                subject_name.append(sub_name)

        stu_table=ttk.Treeview(f8,columns=("teach_id","teach_name","teach_quali","subject_name"),show="headings")
        style=ttk.Style(f8)
    
        style.theme_use("clam")
        style.configure("Treeview",rowheight=50,font=("Roboto"),background="#96DED1",fieldbackground="#96DED1", foreground="black")
        style.configure("Treeview.Heading",font=("Roboto"))
        stu_table.heading("teach_id",text="Teacher_id")
        stu_table.heading("teach_name",text="Teacher_name")
        stu_table.heading("teach_quali",text="Teacher_quali")
        stu_table.heading("subject_name",text="Subject")

        stu_table.column("teach_id",width=200,anchor=CENTER)
        stu_table.column("teach_name",width=250,anchor=CENTER)
        stu_table.column("teach_quali",width=200,anchor=CENTER)
        stu_table.column("subject_name",width=250,anchor=CENTER)

        for i in range(len(teach_name)-1,-1,-1):
                stu_table.insert(parent="",index=0,values=(teach_id[i],teach_name[i],teach_quali[i],subject_name[i]))
        stu_table.pack()

#talk
speaking=False
def talk():
    global speaking
    engine=pyttsx3.init()
    if speaking:
        engine.stop()
        speaking = False
    else:
        speaking = True
        engine.say(summary)
        engine.runAndWait()

#Search Engine
def search_ig():
    input = CTkEntry(f0, width = 350,height=40,font=("halvetica",20),fg_color="#ffe6cc",text_color="black",border_width=3,corner_radius=12,border_color="black",placeholder_text=" Search with StudentHub",placeholder_text_color="grey")
    input.place(x=100,y=90)

    result=''

    def listen():
        messagebox.showinfo("Speak", "Listening...")
        with sr.Microphone() as source:
            r = sr.Recognizer()
            r.adjust_for_ambient_noise(source)  
            audio = r.listen(source, timeout=1) 
            
        try:
            result = r.recognize_google(audio)
            input.delete(0, END)
            input.insert(0, result)
            engine = pyttsx3.init()
            engine.setProperty('rate', 150) 
            engine.say("You said " + result)  
            engine.runAndWait()
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

    def search():
        global result,summary
        result = input.get()
        summary = wikipedia.summary(result, sentences=3)
        text.delete('1.0', END) # clear the text widge
        text.insert('1.0',summary)

    f8=CTkFrame(f0,width=1140,height=501,fg_color="white",border_width=3,corner_radius=2,border_color="black")
    text = tk.Text(f8,font =('halvetica',20),width=94,borderwidth=2,yscrollcommand=10,background="#ffe6cc")

    photo7=CTkImage(Image.open("search_logo.png"),size=(30,30))
    button5 = CTkButton(f0,image=photo7,text='',width=50,height=40,fg_color="#e0e0eb")
    button5.configure(command=search)                                                 
    button5.place(x=450,y=90)

    photo8 = CTkImage(Image.open("mic.png"), size=(30, 30))
    button5 = CTkButton(f0, image=photo8, text='', width=50, height=40, fg_color="#e0e0eb",command=listen)
    button5.place(x=510, y=90)

    photo8 = CTkImage(Image.open("speaker.png"), size=(30, 30))
    button5 = CTkButton(f0, image=photo8, text='', width=50, height=40, fg_color="#e0e0eb",command=talk)
    button5.place(x=570, y=90)

    text.place(x=2,y=0)
    f8.place(x=70,y=140)

#quotes
def quotes():
    try:
        # create a list of quotes
        quotes = [
            "Be the change you wish to see in the world.",
            "The only way to do great work is to love what you do.",
            "Not all who wander are lost.",
            "Believe you can and you're halfway there.",
            "If you want to go fast, go alone. If you want to go far, go together.",
            "It does not matter how slowly you go as long as you do not stop.",
            "Life is what happens when you're busy making other plans.",
            "It is during our darkest moments that we must focus to see the light.",
            "You must be the change you wish to see in the world.",
            "The future belongs to those who believe in the beauty of their dreams.",
            "The best way to predict the future is to invent it."]

        # randomly select a quote from the list
        selected_quote = random.choice(quotes)

        label=CTkLabel(f6,text=selected_quote ,width=40,height=50,font=("bold",18),text_color="black",bg_color="transparent")
        label.place(relx=0.5,rely=0.7,anchor=CENTER)
        quotes_lb=CTkLabel(f6,text="Thought of the day!",width=50,height=20,font=("bold",30),text_color="black",bg_color="transparent")
        quotes_lb.place(relx=0.5,rely=0.3,anchor=CENTER)
        quotes_wall=CTkImage(Image.open("qoutes_bg.png"),size=(70,70))
        quotes_wlb=CTkLabel(f6,text="",image=quotes_wall,width=50,height=20,bg_color="transparent")
        quotes_wlb.place(relx=0.1,rely=0.27,anchor=CENTER)
    except Exception as e:
        pass

#identiy card
def id_card(student_id):
    global f6,Std
    cursor=db.cursor()
    query1=f"Select * from student where stud_id={student_id}"
    cursor.execute(query1)
    s_data=cursor.fetchall()
    data1=s_data[0]
            
    su_id=data1.get("stud_id")
    Name=data1.get("name")
    Dob=data1.get("dob")
    Std=data1.get("std_code")
    Address=data1.get("address")
    mobile=data1.get("phone_no")

    l2=CTkLabel(f0,text=("Welcome "+ Name),font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
    l2.place(x=55,y=20)

    #attendence graph 
    f6=CTkFrame(f0,width=550,height=180,fg_color="#ffe6cc",border_width=3,corner_radius=12,border_color="black")
    f6.place(x=55,y=90)
    quotes()
    f7=CTkFrame(f0,width=590,height=380,fg_color="#ffffe6",border_width=3,corner_radius=12,border_color="black")
    f7.place(x=630,y=90)
        
    photo5=CTkImage(Image.open("id_back.png"),size=(575,170))
    l3=CTkLabel(f7,image=photo5,text="")
    l3.place(x=6,y=5)
    photo6=CTkImage(Image.open("background.jpeg"),size=(575,20))
    l3=CTkLabel(f7,image=photo6,text="")
    l3.place(x=7,y=347)

    f9=CTkFrame(f7,width=160,height=160,border_width=3,corner_radius=12,border_color="black")
    f9.place(x=310,y=110)

    photo6=CTkImage(Image.open("student_photo.png"),size=(150,150))
    l4=CTkLabel(f7,image=photo6,text=" ")
    l4.place(x=315,y=115)

    photo7=CTkImage(Image.open("logo2.png"),size=(70,70))
    l5=CTkLabel(f7,image=photo7,text=" ",bg_color='#6FD0FE')
    l5.place(x=60,y=15)

    l6=CTkLabel(f7,text="IDENTITY CARD",bg_color='#6FD0FE',font=("Helvetica",25),text_color="black")
    l6.place(x=170,y=33)

    id_lb=CTkLabel(f7,text=("STU.ID :  " + str(su_id)),width=100,height=35,corner_radius=8,font=("Helvetica",15),text_color="black",bg_color="#ffffe6")
    id_lb.place(x=15,y=135)

    name_lb=CTkLabel(f7,text=("NAME :   " + Name),width=100,height=35,corner_radius=8,font=("Helvetica",15),text_color="black",bg_color="#ffffe6")
    name_lb.place(x=15,y=170)

    dob_lb=CTkLabel(f7,text=("DOB    :  " + str(Dob)),width=100,height=35,corner_radius=8,font=("Helvetica",15),text_color="black",bg_color="#ffffe6")
    dob_lb.place(x=15,y=205)

    std_lb=CTkLabel(f7,text=("STD    :  "+ Std),width=100,height=35,corner_radius=8,font=("Helvetica",15),text_color="black",bg_color="#ffffe6")
    std_lb.place(x=15,y=240)

    mobile_lb=CTkLabel(f7,text=("MOBILE NO. :  " + str(mobile)),width=100,height=35,corner_radius=8,font=("Helvetica",15),text_color="black",bg_color="#ffffe6")
    mobile_lb.place(x=15,y=275)

    address_lb=CTkLabel(f7,text=("ADDRESS :  " + Address),width=100,height=35,corner_radius=8,font=("Helvetica",15),text_color="black",bg_color="#ffffe6")
    address_lb.place(x=15,y=310)

#to delete frames
def delete_frames():
    for f in f0.winfo_children():
        f.destroy()

#to indicate
def indicate(lb,frame):
    hide_indicators()
    lb.configure(fg_color="#0066ff")
    delete_frames()
    frame()

#hide indicators
def hide_indicators():
    home_indicate.configure(fg_color="white")
    search_indicate.configure(fg_color="white")
    schedule_indicate.configure(fg_color="white")
    complain_indicate.configure(fg_color="white")
    '''logout_indicate.configure(fg_color="white")'''


#--------------------------------------------home frames code -----------------------------------------------------------------------------------

#home_frame
def home_frame(): 
    #date and time 
    id_card(student_id)
    date_time_display()
    f8=CTkFrame(f0,width=550,height=350,fg_color="#ccb3ff",border_width=3,corner_radius=12,border_color="black")
    f8.place(x=55,y=300)
    l2=CTkLabel(f8,text="About School!",font=CTkFont(family="Helvetica",weight="bold",size=30),text_color="black")
    l2.place(x=40,y=30)
    about_text=CTkLabel(f8,text="\nSince 1982 we are working for education to strengthen the \nfuture of our all dear children.We aim to work in building 21st\ncentury skills as it is the call of the modernised future.Our\nVision is to provide education at an impactable scale\nand create the education awareness as far as possible.",font=CTkFont(family="Helvetica",size=20),height=200,width=40,text_color="black",bg_color="#ccb3ff")
    about_text.place(x=5,y=75)

#search_frame
def search_frame():
    global result

    #date and time 
    date_time_display()
    #student section
    l2=CTkLabel(f0,text="Search with StudentHub",font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
    l2.place(x=55,y=20)
    search_ig()

#-------------------------------------------------------------Taught_frame-----------------------------------------------------------------------

#Taught by teacher
def Schedule():
    #date and time 
    date_time_display()

    #teacher_section
    l2=CTkLabel(f0,text="Taught by!",font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
    l2.place(x=55,y=20)

    #table to see teacher details 
    treeview()

#Complain_frame
def complain_frame():
    date_time_display()
    #All complains
    

'''#logout_frame
def logout_frame():
    date_time_display()
    def destroy_student():
        student_win.destroy()
        #login_page()
    #asking to logout
    log_lb=CTkLabel(f0,text="Do you want to logout ?",font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
    log_lb.place(relx=0.4,y=200,anchor=CENTER)
    log_bu=CTkButton(f0,text="Yes",height=45,command=destroy_student,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    log_bu.place(relx=0.4,y=300,anchor=CENTER)'''


#------------------------------------------------------main window code ----------------------------------------------------------------------

#main window
def main_window():
    global f0,student_id,home_indicate,search_indicate,schedule_indicate,complain_indicate,logout_indicate,student_win
    set_appearance_mode("light")
    set_default_color_theme("blue")
    student_win=CTk()
    student_win.title("Student home page")
    screen_width = student_win.winfo_screenwidth()
    screen_height= student_win.winfo_screenheight()
    student_win_width = screen_width
    student_win_height = screen_height
    student_win.geometry(f"{student_win_width}x{student_win_height}")
    student_win.geometry("+0+0")
    student_win.maxsize(width=1400,height=750)
    student_win.minsize(width=1400,height=750) 
    #student_win.attributes('-fullscreen',True)
    frame=CTkFrame(student_win,width=1900,height=1000,fg_color="#66B3FF")
    frame.pack()
    #Home frame
    f0=CTkFrame(frame,width=1400,height=700,fg_color="#66B3FF")
    f0.place(x=140,y=30)
    #Dashboard
    f1=CTkFrame(frame,width=100,height=680,fg_color="white",border_width=3,corner_radius=15,border_color="black")
    f1.place(x=50,y=35)
    #logo
    photo=CTkImage(Image.open("logo2.png"),size=(60,60))
    l1=CTkLabel(f1,image=photo,text=" ")
    l1.place(x=18,y=40)

    #home indicator
    home_indicate=CTkLabel(f1,fg_color="white",text=" ",height=60,width=6)
    home_indicate.place(x=10,y=150)
    
    search_indicate=CTkLabel(f1,fg_color="white",text=" ",height=60,width=6)
    search_indicate.place(x=10,y=250)
    
    schedule_indicate=CTkLabel(f1,fg_color="white",text=" ",height=60,width=6)
    schedule_indicate.place(x=10,y=350)

    complain_indicate=CTkLabel(f1,fg_color="white",text=" ",height=60,width=6)
    complain_indicate.place(x=10,y=450)
    
    #to initialize the student_win
    indicate(home_indicate,home_frame)
    #home button
    photo1=CTkImage(Image.open("home.png"),size=(50,50))
    b1=CTkButton(f1,command=lambda: indicate(home_indicate,home_frame),image=photo1,text="",hover_color="#E0E0EB",cursor="hand2",width=20,height=40,fg_color="white")
    b1.place(x=17,y=150)
    #search button
    photo2=CTkImage(Image.open("search_logo.png"),size=(50,50))
    b2=CTkButton(f1,command=lambda: indicate(search_indicate,search_frame),image=photo2,text=" ",hover_color="#E0E0EB",cursor="hand2",width=15,height=40,fg_color="white")
    b2.place(x=15,y=250)
    #taught_by button 
    photo3=CTkImage(Image.open("Schedule.png"),size=(50,50))
    b2=CTkButton(f1,command=lambda: indicate(schedule_indicate,Schedule),image=photo3,text=" ",hover_color="#E0E0EB",cursor="hand2",width=15,height=40,fg_color="white")
    b2.place(x=15,y=350)
    #Complain button
    photo5=CTkImage(Image.open("report.png"),size=(50,50))
    b2=CTkButton(f1,command=lambda: indicate(complain_indicate,complain_frame),image=photo5,text=" ",hover_color="#E0E0EB",cursor="hand2",width=15,height=40,fg_color="white")
    b2.place(x=15,y=450)

    student_win.mainloop()

main_window()
