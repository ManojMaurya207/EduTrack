from customtkinter import *
import pymysql
from datetime import *
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk,Image
import time 
import random
teacher_id=501

set_appearance_mode("light")
set_default_color_theme("blue")
teacher_win=CTk()
teacher_win.title("Teacher home page")
screen_width = teacher_win.winfo_screenwidth()
screen_height= teacher_win.winfo_screenheight()
teacher_win_width = screen_width
teacher_win_height = screen_height
teacher_win.geometry(f"{teacher_win_width}x{teacher_win_height}")

teacher_win.geometry("+0+0")
teacher_win.maxsize(width=1400,height=750)
teacher_win.minsize(width=1400,height=750)
#teacher_win.attributes('-fullscreen',True)

frame=CTkFrame(teacher_win,width=1920,height=1080,fg_color="#66B3FF")
frame.pack()

#first connection 
db=pymysql.connect(host="localhost",user="root",password="root",database="student_database",charset="utf8mb4",cursorclass=pymysql.cursors.DictCursor)

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
                teacher_win.destroy()
            
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

#Home frame
f0=CTkFrame(frame,width=1200,height=700,fg_color="#66B3FF")
f0.place(x=140,y=30)

#Dashboard
f1=CTkFrame(frame,width=100,height=680,fg_color="white",border_width=3,corner_radius=15,border_color="black")
f1.place(x=50,y=30)

#logo
photo=CTkImage(Image.open("logo2.png"),size=(60,60))
l1=CTkLabel(f1,image=photo,text=" ")
l1.place(x=18,y=40)

#hide indicators
def hide_indicators():
    home_indicate.configure(fg_color="white")
    student_indicate.configure(fg_color="white")
    teacher_indicate.configure(fg_color="white")
    grade_indicate.configure(fg_color="white")

#to delete frames
def delete_frames():
    for f in f0.winfo_children():
        f.destroy()













def id_card(teacher_id):
    cursor=db.cursor()
    query1=f"Select * from teacher where teacher_id={teacher_id}"
    cursor.execute(query1)
    data0=cursor.fetchall()
    data1=data0[0]
        
    tr_id=data1["teacher_id"]
    Name=data1["name"]
    Dob=data1["dob"]
    quali=data1["quali"]
    Address=data1["address"]
    mobile=data1["phone_no"]

    l2=CTkLabel(f0,text=("Welcome "+ Name),font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
    l2.place(x=55,y=20)
    f7=CTkFrame(f0,width=590,height=380,fg_color="#ffffe6",border_width=3,corner_radius=12,border_color="black")
    f7.place(x=580,y=100)
    photo5=CTkImage(Image.open("id_back.png"),size=(575,170))
    l3=CTkLabel(f7,image=photo5,text="")
    l3.place(x=6,y=5)
    photo6=CTkImage(Image.open("background.jpeg"),size=(575,20))
    l3=CTkLabel(f7,image=photo6,text="")
    l3.place(x=7,y=347)
    f9=CTkFrame(f7,width=160,height=160,border_width=3,corner_radius=12,border_color="black")
    f9.place(x=310,y=110)
    photo6=CTkImage(Image.open("teacher_photo.png"),size=(150,150))
    l4=CTkLabel(f7,image=photo6,text=" ")
    l4.place(x=315,y=115)
    photo7=CTkImage(Image.open("logo2.png"),size=(70,70))
    
    l5=CTkLabel(f7,image=photo7,text=" ",bg_color='#6FD0FE')
    l5.place(x=60,y=15)
    l6=CTkLabel(f7,text="IDENTITY CARD",bg_color='#6FD0FE',font=("Helvetica",25),text_color="black")
    l6.place(x=170,y=33)
    id_lb=CTkLabel(f7,text=("TEACHER.ID :  " + str(tr_id)),width=100,height=35,corner_radius=8,font=("Helvetica",15),text_color="black",bg_color="#ffffe6")
    id_lb.place(x=15,y=135)
    name_lb=CTkLabel(f7,text=("NAME :   " + Name),width=100,height=35,corner_radius=8,font=("Helvetica",15),text_color="black",bg_color="#ffffe6")
    name_lb.place(x=15,y=170)
    dob_lb=CTkLabel(f7,text=("DOB    :  " + str(Dob)),width=100,height=35,corner_radius=8,font=("Helvetica",15),text_color="black",bg_color="#ffffe6")
    dob_lb.place(x=15,y=205)
    std_lb=CTkLabel(f7,text=("Quali  : "+ quali),width=100,height=35,corner_radius=8,font=("Helvetica",15),text_color="black",bg_color="#ffffe6")
    std_lb.place(x=15,y=240)
    mobile_lb=CTkLabel(f7,text=("MOBILE NO. :  " + str(mobile)),width=100,height=35,corner_radius=8,font=("Helvetica",15),text_color="black",bg_color="#ffffe6")
    mobile_lb.place(x=15,y=275)
    address_lb=CTkLabel(f7,text=("ADDRESS :  " + Address),width=100,height=35,corner_radius=8,font=("Helvetica",15),text_color="black",bg_color="#ffffe6")
    address_lb.place(x=15,y=310)







def quotes():
    try:
        # create a list of quotes
        quotes = [
            "Be the change you wish to see in the world.",
            "I have a dream.",
            "The only way to do great work is to love what you do.",
            "Not all who wander are lost.",
            "Believe you can and you're halfway there.",
            "In three words I can sum up everything I've learned about life: it goes on.",
            "Success is not final, failure is not fatal: it is the courage to continue that counts.",
            "If you want to go fast, go alone. If you want to go far, go together.",
            "It does not matter how slowly you go as long as you do not stop.",
            "Life is what happens when you're busy making other plans.",
            "The greatest glory in living lies not in never falling, but in rising every time we fall.",
            "It is during our darkest moments that we must focus to see the light.",
            "You must be the change you wish to see in the world.",
            "The future belongs to those who believe in the beauty of their dreams.",
            "The best way to predict the future is to invent it.",
            "I can't change the direction of the wind, but I can adjust my sails to always reach my destination."]

        # randomly select a quote from the list
        selected_quote = random.choice(quotes)

        label = CTkLabel(board1, text=selected_quote, width=40, height=50, font=("bold", 15), text_color="white", bg_color="transparent")
        label.place(relx=0.5, rely=0.5, anchor=CENTER)
        quotes_lb = CTkLabel(board1, text=f"QUOTES :", width=50, height=20, font=("bold", 30), text_color="white", bg_color="transparent")
        quotes_lb.place(relx=0.2, rely=0.5, anchor=CENTER)
    except Exception as e:
        pass








































#home_frame
def home_frame():
    global board1
    date_time_display()
    id_card(teacher_id)

    cursor=db.cursor()
    cursor.execute("Select count(*) count from student where std_code=%s",("5th std"))
    data=cursor.fetchall()
    d=data[0]
    tot_st=d["count"]
    #teacher_win.update()
    f3=CTkFrame(f0,width=240,height=110,fg_color="#FFFFCC",border_width=3,corner_radius=12,border_color="black")
    f3.place(x=40,y=98)
    st_no=CTkLabel(f3,text=tot_st,font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
    st_no.place(x=20,y=10)
    t_st=CTkLabel(f3,text="5th STD",font=CTkFont(family="Helvetica",weight="bold",size=25),text_color="black")
    t_st.place(x=20,y=75)

    #no of students in 6th
    cursor.execute("Select count(*) count from student where std_code=%s",("6th std"))
    data=cursor.fetchall()
    d=data[0]
    tot_te=d["count"]
    f4=CTkFrame(f0,width=240,height=110,fg_color="#C7FAC7",border_width=3,corner_radius=12,border_color="black")
    f4.place(x=40,y=230)
    t_no=CTkLabel(f4,text=tot_te,font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
    t_no.place(x=20,y=10)
    t_te=CTkLabel(f4,text="6th STD",font=CTkFont(family="Helvetica",weight="bold",size=25),text_color="black")
    t_te.place(x=20,y=75)

    #no of students in 7th
    cursor.execute("Select count(*) count from student where std_code=%s",("7th std"))
    data=cursor.fetchall()
    d=data[0]
    tot_te=d["count"]
    f4=CTkFrame(f0,width=240,height=110,fg_color="#FFFFCC",border_width=3,corner_radius=12,border_color="black")
    f4.place(x=40,y=360)
    t_no=CTkLabel(f4,text=tot_te,font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
    t_no.place(x=20,y=10)
    t_te=CTkLabel(f4,text="7th STD",font=CTkFont(family="Helvetica",weight="bold",size=25),text_color="black")
    t_te.place(x=20,y=75)

    #no of students in 8th
    cursor.execute("Select count(*) count from student where std_code=%s",("8th std"))
    data=cursor.fetchall()
    d=data[0]
    tot_te=d["count"]
    f4=CTkFrame(f0,width=240,height=110,fg_color="#C7FAC7",border_width=3,corner_radius=12,border_color="black")
    f4.place(x=300,y=98)
    t_no=CTkLabel(f4,text=tot_te,font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
    t_no.place(x=20,y=10)
    t_te=CTkLabel(f4,text="8th STD",font=CTkFont(family="Helvetica",weight="bold",size=25),text_color="black")
    t_te.place(x=20,y=75)
    
    #no of students in 9th
    cursor.execute("Select count(*) count from student where std_code=%s",("9th std"))
    data=cursor.fetchall()
    d=data[0]
    tot_te=d["count"]
    f4=CTkFrame(f0,width=240,height=110,fg_color="#FFFFCC",border_width=3,corner_radius=12,border_color="black")
    f4.place(x=300,y=230)
    t_no=CTkLabel(f4,text=tot_te,font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
    t_no.place(x=20,y=10)
    t_te=CTkLabel(f4,text="9th STD",font=CTkFont(family="Helvetica",weight="bold",size=25),text_color="black")
    t_te.place(x=20,y=75)
    
    #no of students in 10th
    cursor.execute("Select count(*) count from student where std_code=%s",("10th std"))
    data=cursor.fetchall()
    d=data[0]
    tot_te=d["count"]
    f4=CTkFrame(f0,width=240,height=110,fg_color="#C7FAC7",border_width=3,corner_radius=12,border_color="black")
    f4.place(x=300,y=360)
    t_no=CTkLabel(f4,text=tot_te,font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
    t_no.place(x=20,y=10)
    t_te=CTkLabel(f4,text="10th STD",font=CTkFont(family="Helvetica",weight="bold",size=25),text_color="black")
    t_te.place(x=20,y=75)
    #Quotes
    board1=CTkFrame(f0,width=1140,height=110,fg_color="#3b3a30",border_width=5,corner_radius=12,border_color="black")
    board1.place(x=40,y=520)
    quotes()
    
    
    
    

































#student_frame
def attendance_frame():
    date_time_display()

    def hide_hover():
        stand_5.configure(fg_color="#33CCFF")
        stand_6.configure(fg_color="#33CCFF")
        stand_7.configure(fg_color="#33CCFF")
        stand_8.configure(fg_color="#33CCFF")
        stand_9.configure(fg_color="#33CCFF")
        stand_10.configure(fg_color="#33CCFF")
    
    def treeview(query,val):
        f9=CTkFrame(f0,width=900,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
        f9.place(x=300,y=100)
        cursor=db.cursor()
        cursor.execute(query,val)
        data=cursor.fetchall()
        stud_id=[]
        name=[]
        gen=[]
        std=[]
        dob=[]

        for i in data:
                id=i.get("stud_id")
                na=i.get("name")
                ge=i.get("gen")
                st=i.get("std_code")
                bir=i.get("dob")
                stud_id.append(id)
                name.append(na)
                gen.append(ge)
                std.append(st)
                dob.append(bir)

        stu_table=ttk.Treeview(f9,columns=("stud_id","name","gen","std_code","dob"),show="headings",height=13)
        style=ttk.Style(f9)
    

        style.theme_use("clam")
        style.configure("Treeview",rowheight=49,font=("Roboto"),background="#96DED1",fieldbackground="#96DED1", foreground="black")
        style.configure("Treeview.Heading",font=("Roboto"))
        stu_table.heading("name",text="Name")
        stu_table.heading("stud_id",text="Student id")
        stu_table.heading("gen",text="Gender")
        stu_table.heading("std_code",text="Class")
        stu_table.heading("dob",text="Date of Birth")
        stu_table.column("stud_id",width=200,anchor=CENTER)
        stu_table.column("name",width=300,anchor=CENTER)
        stu_table.column("gen",width=150,anchor=CENTER)
        stu_table.column("std_code",width=190,anchor=CENTER)
        stu_table.column("dob",width=250,anchor=CENTER)

        for i in range(len(stud_id)-1,-1,-1):
                stu_table.insert(parent="",index=0,values=(stud_id[i],name[i],gen[i]))
        stu_table.place(relx=0.5,rely=0.5,anchor=CENTER)
        
    l2=CTkLabel(f0,text="Student Attendence",font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
    l2.place(x=40,y=30)
    f3=CTkFrame(f0,width=240,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
    f3.place(x=40,y=100)

    
    #view details
    def std_5():
        hide_hover()
        stand_5.configure(fg_color="#888888")
        val=("5th std",)
        query="select * from student where std_code = %s"
        treeview(query,val)


    stand_5=CTkButton(f3,hover_color="#888888",command=std_5,text="5th Standard",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    stand_5.place(x=120,y=45,anchor=CENTER)

    def std_6():
        hide_hover()
        stand_6.configure(fg_color="#888888")
        val=("6th std",)
        query="select * from student where std_code = %s"
        treeview(query,val)
    
    stand_6=CTkButton(f3,hover_color="#888888",command=std_6,text="6th Standard",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    stand_6.place(x=120,y=120,anchor=CENTER)


    def std_7():
        hide_hover()
        stand_7.configure(fg_color="#888888")
        val=("7th std",)
        query="select * from student where std_code = %s"
        treeview(query,val)

    stand_7=CTkButton(f3,hover_color="#888888",command=std_7,text="7th Standard",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    stand_7.place(x=120,y=195,anchor=CENTER)

    #update student
    def std_8():
        hide_hover()
        stand_8.configure(fg_color="#888888")
        val=("8th std",)
        query="select * from student where std_code = %s"
        treeview(query,val)
    stand_8=CTkButton(f3,hover_color="#888888",command=std_8,text="8th Standard",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    stand_8.place(x=120,y=270,anchor=CENTER)

    def std_9():
        hide_hover()
        stand_9.configure(fg_color="#888888")
        val=("9th std",)
        query="select * from student where std_code = %s"
        treeview(query,val)
    stand_9=CTkButton(f3,hover_color="#888888",command=std_9,text="9th Standard",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    stand_9.place(x=120,y=345,anchor=CENTER)

    def std_10():
        hide_hover()
        stand_10.configure(fg_color="#888888")
        val=("10th std",)
        query="select * from student where std_code = %s"
        treeview(query,val)
    stand_10=CTkButton(f3,hover_color="#888888",command=std_10,text="10th Standard",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    stand_10.place(x=120,y=420,anchor=CENTER)




















































#teacher_frame
def timetable_frame():
    date_time_display()
    
    def treeview():
        f9=CTkFrame(f0,width=900,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
        f9.place(x=300,y=100)
        cursor=db.cursor()
        cursor.execute("select class.std_id,subject.sub_name from teacher,class,teach_class,subject where teacher.teacher_id=teach_class.teacher_code and class.std_id=teach_class.std_code and subject.sub_id=teach_class.sub_code and teacher.teacher_id=%s",(teacher_id))
        data=cursor.fetchall()
        std_i=[]
        subject_name=[]

        for i in data:
                teacher_name=i.get("std_id")
                sub_name=i.get("sub_name")
                std_i.append(teacher_name)
                subject_name.append(sub_name)

        stu_table=ttk.Treeview(f9,columns=("std_i","subject_name"),show="headings",height=13)
        style=ttk.Style(f9)
    
        style.theme_use("clam")
        style.configure("Treeview",rowheight=49,font=("Roboto"),background="#dac290",fieldbackground="#dac292", foreground="black")
        style.configure("Treeview.Heading",font=("Roboto"))
        stu_table.heading("std_i",text="Standard")
        stu_table.heading("subject_name",text="Subject")
        stu_table.column("std_i",width=545,anchor=CENTER)
        stu_table.column("subject_name",width=545,anchor=CENTER)

        for i in range(len(std_i)-1,-1,-1):
                stu_table.insert(parent="",index=0,values=(std_i[i],subject_name[i]))
        stu_table.place(relx=0.5,rely=0.5,anchor=CENTER)
        
        
        
        
        
        
    #teacher_section
    l2=CTkLabel(f0,text="Teacher's Timetable",font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
    l2.place(x=40,y=30)
    f3=CTkFrame(f0,width=240,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
    f3.place(x=40,y=100)

    #frame for buttons 

    def hide_hover():
        stand_5.configure(fg_color="#33CCFF")
        stand_6.configure(fg_color="#33CCFF")
        stand_7.configure(fg_color="#33CCFF")
    
    #view details
    def time_tb():
        hide_hover()
        stand_5.configure(fg_color="#888888")
        f8=CTkFrame(f0,width=900,height=560,fg_color="white",border_width=3,corner_radius=12,border_color="black")
        f8.place(x=300,y=100)
        photo1=CTkImage(Image.open("timetable_img.jpg"),size=(885,495))
        lb=CTkLabel(f8,image=photo1,text="",width=890,height=500)
        lb.place(relx=0.5,rely=0.5,anchor=CENTER)

    stand_5=CTkButton(f3,hover_color="#888888",command=time_tb,text="Time Table",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    stand_5.place(x=120,y=45,anchor=CENTER)

    def my_sub():
        hide_hover()
        stand_6.configure(fg_color="#888888")
        treeview()
    stand_6=CTkButton(f3,hover_color="#888888",command=my_sub,text="My Classes",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    stand_6.place(x=120,y=120,anchor=CENTER)


    def about():
        hide_hover()
        stand_7.configure(fg_color="#888888")
        f8=CTkFrame(f0,width=900,height=560,fg_color="#ccb3ff",border_width=3,corner_radius=12,border_color="black")
        f8.place(x=300,y=100)
        l2=CTkLabel(f8,text="About Us!",font=CTkFont(family="Helvetica",weight="bold",size=30),text_color="black")
        l2.place(x=40,y=30)
        about_text=CTkLabel(f8,text="\nSince 1982 we are working for education to strengthen the future of our all dear children.\n\nWe aim to work in building 21st century skills as it is the call of the modernised future.\n\nOur Vision is to provide education at a impactable scale and create the education awareness\n\n as far as possible.",font=CTkFont(family="Helvetica",size=20),height=50,width=100,text_color="black")
        about_text.place(x=40,y=100)        
    stand_7=CTkButton(f3,hover_color="#888888",command=about,text="About",height=45,width=170,border_width=2,corner_radius=20,border_color="black",text_color="black",fg_color= "#33CCFF",font=CTkFont("Helvetica",20))
    stand_7.place(x=120,y=195,anchor=CENTER)



#to indicate
def indicate(lb,frame):
    hide_indicators()
    lb.configure(fg_color="#0066ff")
    delete_frames()
    frame()

#grade_frame
def grade_frame():
    date_time_display()
    #asking to grade
    log_lb=CTkLabel(f0,text="GRADES",font=CTkFont(family="Helvetica",weight="bold",size=50),text_color="black")
    log_lb.place(relx=0.5,y=200,anchor=CENTER)
    






#home indicator
home_indicate=CTkLabel(f1,fg_color="white",text=" ",height=60,width=6)
home_indicate.place(x=10,y=150)
#student indicator
student_indicate=CTkLabel(f1,fg_color="white",text=" ",height=60,width=6)
student_indicate.place(x=10,y=250)
#teacher indicator
teacher_indicate=CTkLabel(f1,fg_color="white",text=" ",height=60,width=6)
teacher_indicate.place(x=10,y=350)

#grade indicator
grade_indicate=CTkLabel(f1,fg_color="white",text=" ",height=60,width=6)
grade_indicate.place(x=10,y=450)

#to initialize the teacher_win
indicate(home_indicate,home_frame)

#home button
photo1=CTkImage(Image.open("home.png"),size=(50,50))
b1=CTkButton(f1,command=lambda: indicate(home_indicate,home_frame),image=photo1,text="",hover_color="#E0E0EB",cursor="hand2",width=20,height=40,fg_color="white")
b1.place(x=17,y=150)

#student button
photo2=CTkImage(Image.open("attendence.png"),size=(50,50))
b2=CTkButton(f1,command=lambda: indicate(student_indicate,attendance_frame),image=photo2,text=" ",hover_color="#E0E0EB",cursor="hand2",width=15,height=40,fg_color="white")
b2.place(x=15,y=250)

#teacher button 
photo3=CTkImage(Image.open("time_table.png"),size=(50,50))
b2=CTkButton(f1,command=lambda: indicate(teacher_indicate,timetable_frame),image=photo3,text=" ",hover_color="#E0E0EB",cursor="hand2",width=15,height=40,fg_color="white")
b2.place(x=15,y=350)

#grade button 
photo4=CTkImage(Image.open("grade.png"),size=(50,50))
b2=CTkButton(f1,command=lambda: indicate(grade_indicate,grade_frame),image=photo4,text=" ",hover_color="#E0E0EB",cursor="hand2",width=15,height=40,fg_color="white")
b2.place(x=15,y=450)

teacher_win.mainloop()